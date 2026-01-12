import logging
import os
import threading
import time

from django.apps import AppConfig
from django.conf import settings

from .tasks import notify_winners_for_ended_auctions

logger = logging.getLogger(__name__)
_worker_started = False
_worker_lock = threading.Lock()


def _should_start_worker() -> bool:
    if settings.DEBUG and os.environ.get("RUN_MAIN") != "true":
        return False
    return True


def _notification_worker() -> None:
    while True:
        try:
            notify_winners_for_ended_auctions()
        except Exception:
            logger.exception("Failed to notify auction winners.")
        time.sleep(60)


class AuctionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auctions'

    def ready(self) -> None:
        global _worker_started
        if not _should_start_worker():
            return
        with _worker_lock:
            if _worker_started:
                return
            worker = threading.Thread(
                target=_notification_worker,
                name="auction-winner-notifier",
                daemon=True,
            )
            worker.start()
            _worker_started = True
