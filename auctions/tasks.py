from __future__ import annotations

from typing import List

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
import logging
from .models import Item
from .services import select_winning_bid

logger = logging.getLogger(__name__)

def _mark_winner_notified(item: Item, now: timezone.datetime) -> None:
    item.winner_notified_at = now
    item.save(update_fields=['winner_notified_at'])


def _send_winner_email(item: Item) -> bool:
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        logger.warning(
            "email is not set"
            "set the email or password properly"
        )
        return False
    winning_bid = select_winning_bid(item)
    if winning_bid is None:
        return False

    winner = winning_bid.bidder
    subject = f"You won the auction for {item.title}"
    message = (
        f"Congratulations! You won the auction for '{item.title}' "
        f"with a bid of {winning_bid.amount}."
    )
    sent_count = send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[winner.email],
        fail_silently=False,
    )

    if sent_count < 1:
        logger.warning(
            "Winner email for item %s was not sent (recipient=%s).",
            item.id,
            winner.email,
        )
        return False
    return True


def notify_winner_for_item(item_id: int) -> bool:
    now = timezone.now()
    with transaction.atomic():
        item = (
            Item.objects.select_related('owner')
            .select_for_update()
            .filter(pk=item_id)
            .first()
        )
        if item is None or item.winner_notified_at or item.end_time > now:
            return False

        if select_winning_bid(item) is None:
            _mark_winner_notified(item, now)
            return False

        if not _send_winner_email(item):
            return False
        _mark_winner_notified(item, now)
        return True


def notify_winners_for_ended_auctions() -> List[int]:
    now = timezone.now()
    items = Item.objects.select_related('owner').filter(
        end_time__lte=now,
        winner_notified_at__isnull=True,
    )
    notified_ids: List[int] = []

    for item in items:
        with transaction.atomic():
            locked_item = (
                Item.objects.select_related('owner')
                .select_for_update()
                .filter(pk=item.id, winner_notified_at__isnull=True)
                .first()
            )
            if locked_item is None:
                continue

            if select_winning_bid(locked_item) is None:
                _mark_winner_notified(locked_item, now)
                continue

            if not _send_winner_email(locked_item):
                continue
            _mark_winner_notified(locked_item, now)
            notified_ids.append(locked_item.id)

    return notified_ids