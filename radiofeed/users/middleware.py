from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from radiofeed.common.decorators import middleware
from radiofeed.common.types import GetResponse


@middleware
def language_middleware(
    request: HttpRequest, get_response: GetResponse
) -> HttpResponse:
    """Sets language cookie based on user preferences."""
    response = get_response(request)
    if request.user.is_authenticated:
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, request.user.language)

    return response
