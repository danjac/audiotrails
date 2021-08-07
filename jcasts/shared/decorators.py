from __future__ import annotations

import functools

from typing import Callable

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden


def hx_login_required(view: Callable, next_url: str | None = None) -> Callable:
    @functools.wraps(view)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)

        if request.htmx:
            response = HttpResponseForbidden()
            response["HX-Redirect"] = redirect_to_login(
                next_url or settings.HOME_URL, redirect_field_name=REDIRECT_FIELD_NAME
            ).url
            response["HX-Refresh"] = "true"
            return response

        raise PermissionDenied

    return wrapper
