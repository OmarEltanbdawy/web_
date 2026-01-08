from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            'Profile',
            {
                'fields': (
                    'profile_image',
                    'date_of_birth',
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Profile',
            {
                'fields': (
                    'profile_image',
                    'date_of_birth',
                )
            },
        ),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
