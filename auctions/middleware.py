import logging
import threading
from datetime import datetime, timedelta

from django.utils import timezone

logger = logging.getLogger(__name__)
_last_notification_run: datetime | None = None
_run_lock = threading.Lock()


class AuctionWinnerNotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._maybe_notify_winners()
        return self.get_response(request)

    def _maybe_notify_winners(self) -> None:
        now = timezone.now()
        with _run_lock:
            if _last_notification_run and now - _last_notification_run < timedelta(minutes=1):
                return
            self._set_last_run(now)

        from .tasks import notify_winners_for_ended_auctions

        try:
            notify_winners_for_ended_auctions()
        except Exception:
            logger.exception("Failed to notify auction winners.")

    def _set_last_run(self, now: datetime) -> None:
        global _last_notification_run
        _last_notification_run = now