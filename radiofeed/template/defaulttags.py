import collections
import json
from typing import Any, Optional
from urllib import parse

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import resolve_url
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from radiofeed.typing import ContextDict

from .html import clean_html_content
from .html import stripentities as _stripentities

register = template.Library()


ActiveLink = collections.namedtuple("ActiveLink", "url match exact")


json_escapes = {
    ord(">"): "\\u003E",
    ord("<"): "\\u003C",
    ord("&"): "\\u0026",
    ord("'"): "\\u0027",
}


@register.simple_tag(takes_context=True)
def active_link(context: ContextDict, url_name: str, *args, **kwargs) -> ActiveLink:
    url = resolve_url(url_name, *args, **kwargs)
    if context["request"].path == url:
        return ActiveLink(url, True, True)
    elif context["request"].path.startswith(url):
        return ActiveLink(url, True, False)
    return ActiveLink(url, False, False)


@register.inclusion_tag("_share.html", takes_context=True)
def share_buttons(context: ContextDict, url: str, subject: str):
    url = parse.quote(context["request"].build_absolute_uri(url))
    subject = parse.quote(subject)

    return {
        "share_urls": {
            "email": f"mailto:?subject={subject}&body={url}",
            "facebook": f"https://www.facebook.com/sharer/sharer.php?u={url}",
            "twitter": f"https://twitter.com/share?url={url}&text={subject}",
            "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={url}",
        }
    }


@register.filter
@stringfilter
def clean_html(value: str) -> str:
    return mark_safe(_stripentities(clean_html_content(value or "")))


@register.filter
@stringfilter
def stripentities(value: str) -> str:
    return _stripentities(value or "")


@register.filter
def percent(value: Optional[float], total: Optional[float]) -> float:
    if not value or not total:
        return 0

    return (value / total) * 100


@register.filter
def jsonify(value: Any) -> str:
    return mark_safe(json.dumps(value, cls=DjangoJSONEncoder).translate(json_escapes))
