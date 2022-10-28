from __future__ import annotations

import collections
import math

from urllib import parse

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import resolve_url
from django.template.context import Context, RequestContext
from django.template.defaultfilters import stringfilter
from django.utils.translation import gettext as _

from radiofeed.common import markup, pagination

register = template.Library()

ActiveLink = collections.namedtuple("ActiveLink", ["url", "css", "active"])


_validate_url = URLValidator(["http", "https"])


@register.simple_tag(takes_context=True)
def pagination_url(context: RequestContext, *args, **kwargs) -> str:
    """Inserts the "page" query string parameter with the provided page number into the template.

    Preserves the original request path and any other query string parameters.

    Given the above and a URL of "/search?q=test" the result would
    be something like: "/search?q=test&page=3"

    Returns:
        updated URL path with new page
    """
    return pagination.pagination_url(context.request, *args, **kwargs)


@register.simple_tag
def get_contact_email() -> str:
    """Returns CONTACT_EMAIL setting."""
    return settings.CONTACT_EMAIL


@register.simple_tag(takes_context=True)
def absolute_uri(
    context: Context,
    url: str | None = None,
    *args,
    **kwargs,
) -> str:
    """Generate absolute URI based on server environment or current Site."""
    url = resolve_url(url, *args, **kwargs) if url else None

    if request := context.get("request", None):
        return request.build_absolute_uri(url)

    # in case we don't have a request, e.g. in email job
    protocol = "https" if settings.SECURE_SSL_REDIRECT else "http"
    base_url = f"{protocol}://{Site.objects.get_current().domain}"
    return parse.urljoin(base_url, url) if url else base_url


@register.filter
def format_duration(total_seconds: int | None) -> str:
    """Formats duration (in seconds) as human readable value e.g. 1h 30min."""
    if total_seconds is None or total_seconds < 60:
        return ""

    rv: list[str] = []

    if total_hours := math.floor(total_seconds / 3600):
        rv.append(_("{total_hours}h").format(total_hours=total_hours))

    if total_minutes := round((total_seconds % 3600) / 60):
        rv.append(_("{total_minutes}min").format(total_minutes=total_minutes))

    return " ".join(rv)


@register.simple_tag(takes_context=True)
def active_link(
    context: RequestContext,
    url_name: str,
    css="link",
    active_css="active",
    *args,
    **kwargs,
) -> ActiveLink:
    """Returns url with active link info."""
    url = resolve_url(url_name, *args, **kwargs)

    return (
        ActiveLink(url, f"{css} {active_css}", True)
        if context.request.path == url
        else ActiveLink(url, css, False)
    )


@register.inclusion_tag("includes/markdown.html")
def markdown(value: str | None) -> dict:
    """Renders Markdown or HTML content."""
    return {"content": markup.markup(value)}


@register.inclusion_tag("includes/cookie_notice.html", takes_context=True)
def cookie_notice(context: RequestContext) -> dict:
    """Renders GDPR cookie notice. Notice should be hidden once user has clicked "Accept Cookies" button."""
    return {"accept_cookies": "accept-cookies" in context.request.COOKIES}


@register.inclusion_tag("includes/icon.html")
def icon(
    name: str, style: str = "", *, size="", title: str = "", css_class: str = ""
) -> dict:
    """Renders a FontAwesome icon."""
    return {
        "name": name,
        "style": f"fa-{style}" if style else "fa",
        "size": f"fa-{size}" if size else "",
        "title": title,
        "css_class": css_class,
    }


@register.filter
@stringfilter
def normalize_url(url: str) -> str:
    """If a URL is provided minus http(s):// prefix, prepends protocol."""
    if url:
        for value in (url, f"https://{url}"):
            try:
                _validate_url(value)
                return value
            except ValidationError:
                continue
    return ""
