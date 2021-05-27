import functools

from typing import Callable

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse


def ajax_login_required(view: Callable) -> Callable:
    @functools.wraps(view)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        raise PermissionDenied

    return wrapper
