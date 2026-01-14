from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional, TypedDict

from accounts.models import User


class ProfilePayload(TypedDict):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    date_of_birth: Optional[str]
    profile_image_url: Optional[str]


@dataclass(frozen=True)
class ProfileUpdate:
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    date_of_birth: Optional[date] = None


def user_to_profile_payload(user: User) -> ProfilePayload:
    return ProfilePayload(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth.isoformat() if user.date_of_birth else None,
        profile_image_url=user.profile_image.url if user.profile_image else None,
    )
