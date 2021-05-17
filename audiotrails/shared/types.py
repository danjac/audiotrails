from typing import TYPE_CHECKING, Any, Protocol, Union

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet
from django.http import HttpRequest

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser as AuthenticatedUser
else:
    AuthenticatedUser = get_user_model()

ContextDict = dict[str, Any]

AnyUser = Union[AuthenticatedUser, AnonymousUser]


class ActionProtocol(Protocol):
    def __call__(
        modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet
    ) -> str:
        ...

    short_description: str
    boolean: bool


def admin_action(func: Any) -> ActionProtocol:
    return func
