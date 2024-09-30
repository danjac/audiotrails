from typing import Final

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.functional import SimpleLazyObject

DEFAULT_PAGE_SIZE: Final = 30


def paginate(
    request: HttpRequest,
    object_list: QuerySet,
    page_size: int = DEFAULT_PAGE_SIZE,
    param: str = "page",
    **pagination_kwargs,
) -> SimpleLazyObject:
    """Returns lazily-evaluated pagination object, so the database queries are not evaluated until the page obj is referenced."""

    return SimpleLazyObject(
        lambda: Paginator(object_list, page_size).get_page(
            request.GET.get(param, ""), **pagination_kwargs
        )
    )
