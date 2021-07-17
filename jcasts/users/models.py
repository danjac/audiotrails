from __future__ import annotations

import hashlib

from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserQuerySet(models.QuerySet):
    def for_email(self, email: str) -> models.QuerySet:
        """Returns users matching this email address, including both
        primary and secondary email addresses
        """
        return self.filter(
            models.Q(emailaddress__email__iexact=email) | models.Q(email__iexact=email)
        )

    def matches_usernames(self, names: list[str]) -> models.QuerySet:
        """Returns users matching the (case insensitive) username."""
        if not names:
            return self.none()
        return self.filter(username__iregex=r"^(%s)+" % "|".join(names))


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):  # type: ignore
    def create_user(
        self, username: str, email: str, password: str | None = None, **kwargs
    ) -> User:
        user = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username: str, email: str, password: str, **kwargs
    ) -> User:
        return self.create_user(
            username,
            email,
            password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )


class User(AbstractUser):
    send_recommendations_email: bool = models.BooleanField(default=True)
    autoplay: bool = models.BooleanField(default=True)

    objects = UserManager()

    def get_email_addresses(self) -> set[str]:
        """Get set of emails belonging to user.

        Returns:
            set: set of email addresses
        """
        return {self.email} | set(self.emailaddress_set.values_list("email", flat=True))

    def get_gravatar_url(
        self,
        size: int | str = settings.GRAVATAR_DEFAULT_SIZE,
        default: str = settings.GRAVATAR_DEFAULT_IMAGE,
        rating: str = settings.GRAVATAR_DEFAULT_RATING,
    ) -> str:
        digest = hashlib.md5(self.email.encode("utf-8")).hexdigest()
        qs = urlencode(
            {
                "s": str(size),
                "d": default,
                "r": rating,
            }
        )
        return f"https://www.gravatar.com/avatar/{digest}?{qs}"
