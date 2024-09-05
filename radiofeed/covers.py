import functools
import itertools
import pathlib
import urllib.parse
from enum import StrEnum
from typing import Final

from django.conf import settings
from django.core.signing import Signer
from django.http import HttpRequest
from django.templatetags.static import static
from django.urls import reverse


class CoverVariant(StrEnum):
    """Possible size variations."""

    CARD = "card"
    DETAIL = "detail"
    TILE = "tile"


_COVER_SIZES: Final = {
    CoverVariant.CARD: (96, 96),
    CoverVariant.DETAIL: (144, 160),
    CoverVariant.TILE: (112, 224),
}

_COVER_CLASSES: Final = {
    CoverVariant.CARD: "size-16",
    CoverVariant.DETAIL: "size-36 lg:size-40",
    CoverVariant.TILE: "size-28 lg:size-56",
}

_MIN_FULL_SIZE_WIDTH: Final = 1024


@functools.cache
def get_cover_class(variant: CoverVariant, *classes) -> str:
    """Returns default CSS class for the cover image."""
    return " ".join(
        [
            css_class.strip()
            for css_class in [_COVER_CLASSES[variant], *classes]
            if css_class
        ]
    ).strip()


@functools.cache
def get_cover_attrs(cover_url: str, variant: CoverVariant) -> dict:
    """Returns the HTML attributes for an image."""
    min_size, full_size = _COVER_SIZES[variant]
    full_src = get_cover_url(cover_url, full_size)

    attrs = {
        "height": full_size,
        "width": full_size,
        "src": full_src,
    }

    # no size variations
    if min_size == full_size:
        return attrs

    min_src = get_cover_url(cover_url, min_size)

    srcset = ", ".join(
        [
            f"{full_src} {full_size}w",
            f"{min_src} {min_size}w",
        ]
    )

    sizes = ", ".join(
        [
            f"(max-width: {_MIN_FULL_SIZE_WIDTH-0.01}px) {min_size}px",
            f"(min-width: {_MIN_FULL_SIZE_WIDTH}px) {full_size}px",
        ]
    )

    return attrs | {"srcset": srcset, "sizes": sizes}


@functools.cache
def get_cover_url(cover_url: str | None, size: int) -> str:
    """Return the cover image URL"""
    return (
        (
            reverse(
                "cover_image",
                kwargs={
                    "size": size,
                },
            )
            + "?"
            + urllib.parse.urlencode({"url": Signer().sign(cover_url)})
        )
        if cover_url
        else get_placeholder_url(size)
    )


@functools.cache
def get_placeholder(size: int) -> str:
    """Return placeholder image name"""
    return f"placeholder-{size}.webp"


@functools.cache
def get_placeholder_url(size: int) -> str:
    """Return URL to cover image placeholder"""
    return static(f"img/{get_placeholder(size)}")


@functools.cache
def get_placeholder_path(size: int) -> pathlib.Path:
    """Returns path to placeholder image"""
    return settings.BASE_DIR / "assets" / "img" / get_placeholder(size)


@functools.cache
def is_cover_size(size: int) -> bool:
    """Check image has correct size."""
    return size in get_allowed_sizes()


@functools.cache
def get_allowed_sizes() -> set[int]:
    """Returns set of allowed sizes."""
    return set(itertools.chain.from_iterable(_COVER_SIZES.values()))


def get_metadata_info(request: HttpRequest, cover_url: str | None) -> list[dict]:
    """Returns media artwork details."""
    return [
        {
            "src": request.build_absolute_uri(get_cover_url(cover_url, size)),
            "sizes": f"{size}x{size}",
            "type": "image/webp",
        }
        for size in get_allowed_sizes()
    ]
