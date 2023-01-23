from __future__ import annotations

import html

from typing import Final

import bleach
import markdown

from django.template.defaultfilters import striptags
from django.utils.safestring import mark_safe

_ALLOWED_TAGS: Final = {
    "a",
    "abbr",
    "acronym",
    "address",
    "b",
    "br",
    "div",
    "dl",
    "dt",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "li",
    "ol",
    "p",
    "pre",
    "q",
    "s",
    "small",
    "strike",
    "strong",
    "span",
    "style",
    "sub",
    "sup",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "tr",
    "tt",
    "u",
    "ul",
}

_ALLOWED_ATTRS: Final = {
    "a": ["href", "target", "title"],
}


def clean(value: str | None) -> str:
    """Runs Bleach through value and scrubs any unwanted HTML tags and attributes."""
    return (
        bleach.linkify(
            bleach.clean(
                value,
                attributes=_ALLOWED_ATTRS,
                tags=_ALLOWED_TAGS,
                strip=True,
            ),
            [_linkify_callback],  # type: ignore
        )
        if value
        else ""
    )


def strip_whitespace(value: str | None) -> str:
    """Removes all trailing whitespace."""
    return (value or "").strip()


def strip_html(value: str | None) -> str:
    """Scrubs all HTML tags and entities from text."""
    return html.unescape(striptags(strip_whitespace(value)))


def markup(value: str | None) -> str:
    """Returns safe Markdown rendered string. If content is already HTML will pass as-is."""
    if value := strip_whitespace(value):
        return mark_safe(clean(markdown.markdown(value)))  # nosec
    return ""


def _linkify_callback(attrs: dict, new: bool = False) -> dict:
    attrs[(None, "target")] = "_blank"
    attrs[(None, "rel")] = "noopener noreferrer nofollow"
    return attrs
