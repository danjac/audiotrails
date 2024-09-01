from __future__ import annotations

import functools
import math
from typing import TYPE_CHECKING, Any, Final, TypedDict

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import resolve_url
from django.template.defaultfilters import pluralize
from django.template.loader import get_template

from radiofeed import cover_image, markdown

if TYPE_CHECKING:  # pragma: nocover
    from collections.abc import Iterator

    from django.core.paginator import Page
    from django.template.base import NodeList, Parser, Token
    from django.template.context import Context, RequestContext

    from radiofeed.cover_image import CoverImageVariant


_SECONDS_IN_MINUTE: Final = 60
_SECONDS_IN_HOUR: Final = 3600

register = template.Library()


class ActiveLink(TypedDict):
    """Provides details on whether a link is currently active, along with its
    URL and CSS."""

    url: str
    css: str
    active: bool


@register.simple_tag(takes_context=True)
def active_link(
    context: RequestContext,
    to: Any,
    *,
    css: str = "link",
    active_css: str = "active",
    **kwargs,
) -> ActiveLink:
    """Returns url with active link info if matching URL."""
    url = resolve_url(to, **kwargs)
    return (
        ActiveLink(active=True, css=f"{css} {active_css}", url=url)
        if context.request.path == url
        else ActiveLink(active=False, css=css, url=url)
    )


@register.simple_tag
def theme_color() -> dict:
    """Returns the PWA configuration theme color."""
    return settings.PWA_CONFIG["manifest"]["theme_color"]


@register.simple_tag
@functools.cache
def get_site() -> Site:
    """Returns the current Site instance. Use when `request.site` is unavailable, e.g. in emails run from cronjobs."""

    return Site.objects.get_current()


@register.simple_tag
def absolute_uri(to: Any | None = None, *args, **kwargs) -> str:
    """Returns the absolute URL to site domain."""

    site = get_site()
    path = resolve_url(to, *args, **kwargs) if to else ""
    scheme = "https" if settings.SECURE_SSL_REDIRECT else "http"

    return f"{scheme}://{site.domain}{path}"


get_cover_image_attrs = register.simple_tag(cover_image.get_cover_image_attrs)


@register.inclusion_tag("_cover_image.html", name="cover_image")
def cover_image_(
    cover_url: str | None,
    variant: CoverImageVariant,
    title: str,
    *,
    css_class: str = "",
) -> dict:
    """Renders a cover image with proxy URL."""
    attrs = {
        "alt": title,
        "title": title,
    } | cover_image.get_cover_image_attrs(cover_url, variant)
    css_class = " ".join(
        [
            css_class,
            cover_image.get_cover_image_class(variant),
        ]
    ).strip()
    return {
        "attrs": attrs,
        "cover_url": cover_url,
        "css_class": css_class,
        "title": title,
    }


@register.inclusion_tag("_gdpr_cookies_banner.html", takes_context=True)
def gdpr_cookies_banner(context: RequestContext) -> dict:
    """Renders GDPR cookie notice. Notice should be hidden once user has clicked
    "Accept Cookies" button."""
    return {"accept_cookies": settings.GDPR_COOKIE_NAME in context.request.COOKIES}


@register.inclusion_tag("_markdown.html", name="markdown")
def markdown_(content: str | None) -> dict:
    """Render content as Markdown."""
    return {"content": markdown.render(content or "")}


@register.filter
def format_duration(total_seconds: int | None) -> str:
    """Formats duration (in seconds) as human readable value e.g. 1h 30min."""
    if total_seconds is None or total_seconds < _SECONDS_IN_MINUTE:
        return ""

    rv: list[str] = []

    if total_hours := math.floor(total_seconds / _SECONDS_IN_HOUR):
        rv.append(f"{total_hours} hour{pluralize(total_hours)}")

    if total_minutes := round((total_seconds % _SECONDS_IN_HOUR) / _SECONDS_IN_MINUTE):
        rv.append(f"{total_minutes} minute{pluralize(total_minutes)}")

    return " ".join(rv)


@register.filter
def percentage(value: float, total: float) -> int:
    """Returns % value.

    Example:
    {{ value|percentage:total }}% done
    """
    if 0 in (value, total):
        return 0
    return min(math.ceil((value / total) * 100), 100)


@register.tag
def pagination(parser: Parser, token: Token) -> PaginationNode:
    """Renders paginated list.

    Usage:
        {% pagination page_obj %}
            {% include "podcasts/_podcast.html" with podcast=item %}
        {% endpagination %}
    """
    nodelist = parser.parse(("endpagination",))
    parser.delete_first_token()
    try:
        (page_obj,) = token.contents.split()[1:]
    except ValueError as exc:
        raise template.TemplateSyntaxError(
            "page_obj argument required for pagination tag"
        ) from exc

    return PaginationNode(page_obj, nodelist)


class PaginationNode(template.Node):
    """Implementation of pagination tag."""

    def __init__(
        self,
        page_obj: str,
        nodelist: NodeList,
        request: str = "request",
        template_name: str = "_pagination.html",
    ) -> None:
        self.nodelist = nodelist
        self.template = get_template(template_name)

        self.page_obj = template.Variable(page_obj)
        self.request = template.Variable(request)

    def render(self, context: Context) -> str:
        """Render pagination."""

        page_obj = self.page_obj.resolve(context)
        request = self.request.resolve(context)

        previous_page, next_page = None, None

        if page_obj.has_previous():
            previous_page = page_obj.previous_page_number()

        if page_obj.has_next():
            next_page = page_obj.next_page_number()

        has_other_pages = next_page or previous_page

        with context.push():
            context.update(
                {
                    "previous_page": previous_page,
                    "next_page": next_page,
                    "has_other_pages": has_other_pages,
                    "paginated_items": self._paginated_items(page_obj, context),
                }
            )

            return self.template.render(context.flatten(), request)

    def _paginated_items(self, page_obj: Page, context: Context) -> Iterator[str]:
        for item in page_obj:
            with context.push():
                context.update({"item": item})
                yield self.nodelist.render(context)
