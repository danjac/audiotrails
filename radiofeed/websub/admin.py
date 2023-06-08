from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from radiofeed.websub.models import Subscription


class ModeFilter(admin.SimpleListFilter):
    """Filters subscriptions based on their mode."""

    title = "Verified"
    parameter_name = "verified"

    def lookups(
        self, request: HttpRequest, model_admin: admin.ModelAdmin[Subscription]
    ) -> tuple[tuple[str, str], ...]:
        """Returns lookup values/labels."""
        return (("none", "None"),) + tuple(Subscription.Mode.choices)

    def queryset(
        self, request: HttpRequest, queryset: QuerySet[Subscription]
    ) -> QuerySet[Subscription]:
        """Returns filtered queryset."""

        match self.value():
            case "none":
                return queryset.filter(mode="")

            case value if value in Subscription.Mode:  # type: ignore
                return queryset.filter(mode=value)

            case _:
                return queryset


class RequestedFilter(admin.SimpleListFilter):
    """Filters subscriptions with subscribe request."""

    title = "Requested"
    parameter_name = "requested"

    def lookups(
        self, request: HttpRequest, model_admin: admin.ModelAdmin[Subscription]
    ) -> tuple[tuple[str, str], ...]:
        """Returns lookup values/labels."""
        return (("yes", "Requested"),)

    def queryset(
        self, request: HttpRequest, queryset: QuerySet[Subscription]
    ) -> QuerySet[Subscription]:
        """Returns filtered queryset."""

        if self.value() == "yes":
            return queryset.filter(requested__isnull=False)


class VerifiedFilter(admin.SimpleListFilter):
    """Filters subscriptions with with verified request."""

    title = "Verified"
    parameter_name = "verified"

    def lookups(
        self, request: HttpRequest, model_admin: admin.ModelAdmin[Subscription]
    ) -> tuple[tuple[str, str], ...]:
        """Returns lookup values/labels."""
        return (("yes", "Verified"),)

    def queryset(
        self, request: HttpRequest, queryset: QuerySet[Subscription]
    ) -> QuerySet[Subscription]:
        """Returns filtered queryset."""

        if self.value() == "yes":
            return queryset.filter(verified__isnull=False)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Django admin for Subscription model."""

    list_filter = (
        ModeFilter,
        RequestedFilter,
        VerifiedFilter,
    )

    list_display = ("podcast", "mode", "requested", "verified")
    raw_id_fields = ("podcast",)
    readonly_fields = (
        "podcast",
        "hub",
        "topic",
        "mode",
        "secret",
        "expires",
        "requested",
        "verified",
        "num_retries",
    )
