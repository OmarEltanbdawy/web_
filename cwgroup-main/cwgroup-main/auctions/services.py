from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from django.db.models import Max
from django.utils import timezone

from .models import Bid, Item


@dataclass(frozen=True)
class BidValidationResult:
    is_valid: bool
    reason: str
    minimum_required: Decimal


def is_auction_ended(item: Item) -> bool:
    return timezone.now() >= item.end_time


def get_current_highest_bid(item: Item) -> Optional[Bid]:
    return item.bids.order_by('-amount', 'created_at').first()


def get_current_highest_amount(item: Item) -> Decimal:
    highest = item.bids.aggregate(max_amount=Max('amount')).get('max_amount')
    if highest is None:
        return item.starting_price
    return highest


def validate_bid(item: Item, amount: Decimal) -> BidValidationResult:
    if is_auction_ended(item):
        return BidValidationResult(False, 'Auction has ended.', get_current_highest_amount(item))

    current_amount = get_current_highest_amount(item)
    minimum_required = current_amount
    if amount <= current_amount:
        return BidValidationResult(
            False,
            'Bid must be higher than the current highest amount.',
            minimum_required,
        )

    return BidValidationResult(True, 'Bid accepted.', minimum_required)


def select_winning_bid(item: Item) -> Optional[Bid]:
    if not is_auction_ended(item):
        return None
    return get_current_highest_bid(item)
