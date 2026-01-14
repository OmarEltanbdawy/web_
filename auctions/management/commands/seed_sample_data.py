from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from auctions.models import Item


class Command(BaseCommand):
    help = 'creating admin user, five test users, and ten sample auction items.'

    def handle(self, *args, **options) -> None:
        admin_user = self._create_admin_user()
        test_users = self._create_test_users()
        self._create_sample_items(test_users)

        self.stdout.write(
            self.style.SUCCESS(
                'sample data created. Admin user: ' f'{admin_user.username}'
            )
        )

    def _create_admin_user(self):
        User = get_user_model()
        admin_defaults = {
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True,
        }
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults=admin_defaults,
        )
        if created:
            admin_user.set_password('AdminPass123!')
            admin_user.save(update_fields=['password'])
        else:
            changed = False
            if not admin_user.is_staff or not admin_user.is_superuser:
                admin_user.is_staff = True
                admin_user.is_superuser = True
                changed = True
            if changed:
                admin_user.save(update_fields=['is_staff', 'is_superuser'])
        return admin_user

    def _create_test_users(self):
        User = get_user_model()
        test_users = []
        for index in range(1, 6):
            username = f'testuser{index}'
            email = f'{username}@example.com'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_staff': False,
                    'is_superuser': False,
                },
            )
            if created:
                user.set_password('TestUser123!')
                user.save(update_fields=['password'])
            test_users.append(user)
        return test_users

    def _create_sample_items(self, test_users) -> None:
        sample_items = [
            {
                'title': 'Camera',
                'description': 'film camera',
                'starting_price': Decimal('45.00'),
                'end_time': timezone.now() + timedelta(days=7),
            },
            {
                'title': 'Keyboard',
                'description': 'RGB backlit keyboard',
                'starting_price': Decimal('60.00'),
                'end_time': timezone.now() + timedelta(days=6),
            },
            {
                'title': 'Bike',
                'description': 'nice bike',
                'starting_price': Decimal('30.00'),
                'end_time': timezone.now() + timedelta(days=5),
            },
            {
                'title': 'phone',
                'description': 'beautiful ',
                'starting_price': Decimal('50.00'),
                'end_time': timezone.now() + timedelta(days=4),
            },
            {
                'title': 'speaker',
                'description': 'portable ',
                'starting_price': Decimal('35.00'),
                'end_time': timezone.now() + timedelta(days=8),
            },
            {
                'title': 'Coffee machine',
                'description': 'tasty cofee',
                'starting_price': Decimal('40.00'),
                'end_time': timezone.now() + timedelta(days=9),
            },
            {
                'title': 'dumbells',
                'description': 'very nice',
                'starting_price': Decimal('20.00'),
                'end_time': timezone.now() + timedelta(days=3),
            },
            {
                'title': 'earbuds',
                'description': 'Noise cancelling',
                'starting_price': Decimal('55.00'),
                'end_time': timezone.now() + timedelta(days=10),
            },
            {
                'title': 'LED Desk Lamp',
                'description': 'convinient',
                'starting_price': Decimal('25.00'),
                'end_time': timezone.now() + timedelta(days=2),
            },
            {
                'title': 'pan',
                'description': 'stainless stell',
                'starting_price': Decimal('70.00'),
                'end_time': timezone.now() + timedelta(days=11),
            },
        ]

        for index, item_data in enumerate(sample_items):
            owner = test_users[index % len(test_users)]
            Item.objects.get_or_create(
                owner=owner,
                title=item_data['title'],
                defaults={
                    'description': item_data['description'],
                    'starting_price': item_data['starting_price'],
                    'end_time': item_data['end_time'],
                },
            )
