from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.utils.functional import SimpleLazyObject

from radiofeed.common.decorators import middleware
from radiofeed.common.paginator import Paginator
from radiofeed.common.search import Search
from radiofeed.common.sorter import Sorter
from radiofeed.common.types import GetResponse
from radiofeed.utils.http import user_agent


@middleware
def cache_control_middleware(
    request: HttpRequest, get_response: GetResponse
) -> HttpResponse:
    """Workaround for https://github.com/bigskysoftware/htmx/issues/497.

    Place after HtmxMiddleware.
    """
    response = get_response(request)
    if request.htmx:
        # don't override if cache explicitly set
        response.setdefault("Cache-Control", "no-store, max-age=0")
    return response


@middleware
def paginator_middleware(
    request: HttpRequest, get_response: GetResponse
) -> HttpResponse:
    """Adds Sorter instance to request as `request.sorter`."""
    request.paginator = SimpleLazyObject(lambda: Paginator(request))
    return get_response(request)


@middleware
def search_middleware(request: HttpRequest, get_response: GetResponse) -> HttpResponse:
    """Adds Search instance to request as `request.search`."""
    request.search = SimpleLazyObject(lambda: Search(request))
    return get_response(request)


@middleware
def sorter_middleware(request: HttpRequest, get_response: GetResponse) -> HttpResponse:
    """Adds Sorter instance to request as `request.sorter`."""
    request.sorter = SimpleLazyObject(lambda: Sorter(request))
    return get_response(request)


@middleware
def user_agent_middleware(
    request: HttpRequest, get_response: GetResponse
) -> HttpResponse:
    """Adds Sorter instance to request as `request.sorter`."""
    request.user_agent = SimpleLazyObject(lambda: user_agent(request))
    return get_response(request)
