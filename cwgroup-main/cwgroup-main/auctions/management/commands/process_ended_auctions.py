from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand

from auctions.tasks import notify_winners_for_ended_auctions


class Command(BaseCommand):
    help = 'Detect ended auctions and send winner emails.'

    def handle(self, *args: Any, **options: Any) -> None:
        notified = notify_winners_for_ended_auctions()
        self.stdout.write(self.style.SUCCESS(f"Notified winners for items: {notified}"))
