from __future__ import annotations

from typing import List

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from .models import Item
from .services import select_winning_bid


def notify_winners_for_ended_auctions() -> List[int]:
    now = timezone.now()
    items = Item.objects.select_related('owner').filter(
        end_time__lte=now,
        winner_notified_at__isnull=True,
    )
    notified_ids: List[int] = []

    for item in items:
        winning_bid = select_winning_bid(item)
        if winning_bid is None:
            item.winner_notified_at = now
            item.save(update_fields=['winner_notified_at'])
            continue

        winner = winning_bid.bidder
        subject = f"You won the auction for {item.title}"
        message = (
            f"Congratulations! You won the auction for '{item.title}' "
            f"with a bid of {winning_bid.amount}."
        )
        recipient_list = [winner.email]

        with transaction.atomic():
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            item.winner_notified_at = now
            item.save(update_fields=['winner_notified_at'])
            notified_ids.append(item.id)

    return notified_ids
