import functools
import itertools
import pathlib
import urllib.parse
from typing import Final, Literal

from django.conf import settings
from django.core.signing import Signer
from django.http import HttpRequest
from django.templatetags.static import static
from django.urls import reverse

from radiofeed.manifest import ImageAsset

CoverImageVariant = Literal["card", "detail", "tile"]

_COVER_IMAGE_SIZES: Final[dict[CoverImageVariant, tuple[int, int]]] = {
    "card": (96, 96),
    "detail": (144, 160),
    "tile": (160, 224),
}

_COVER_IMAGE_CLASSES: Final[dict[CoverImageVariant, str]] = {
    "card": "size-16",
    "detail": "size-36 lg:size-40",
    "tile": "size-40 lg:size-56",
}

_MIN_DESKTOP_WIDTH: Final = 1024


@functools.cache
def get_cover_image_attrs(
    variant: CoverImageVariant,
    cover_url: str,
    title: str,
    **attrs: str,
) -> dict:
    """Returns the HTML attributes for an image."""
    min_size, full_size = _COVER_IMAGE_SIZES[variant]
    full_src = get_cover_image_url(cover_url, full_size)

    attrs = {
        "alt": title,
        "title": title,
        "src": full_src,
        "width": full_size,
        "height": full_size,
    } | attrs

    # no size variations
    if min_size == full_size:
        return attrs

    min_src = get_cover_image_url(cover_url, min_size)

    srcset = ", ".join(
        [
            f"{full_src} {full_size}w",
            f"{min_src} {min_size}w",
        ]
    )

    sizes = ", ".join(
        [
            f"(max-width: {_MIN_DESKTOP_WIDTH-0.01}px) {min_size}px",
            f"(min-width: {_MIN_DESKTOP_WIDTH}px) {full_size}px",
        ]
    )

    return attrs | {"srcset": srcset, "sizes": sizes}


@functools.cache
def get_cover_image_url(cover_url: str, size: int) -> str:
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
def get_cover_image_class(variant: CoverImageVariant, *classes: str) -> str:
    """Returns default CSS class for the cover image."""
    return " ".join([*[_COVER_IMAGE_CLASSES[variant]], *list(classes)])


@functools.cache
def is_cover_image_size(size: int) -> bool:
    """Check image has correct size."""
    return size in get_cover_image_sizes()


@functools.cache
def get_cover_image_sizes() -> set[int]:
    """Returns set of allowed sizes."""
    return set(itertools.chain.from_iterable(_COVER_IMAGE_SIZES.values()))


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
    return settings.STATIC_SRC / "img" / get_placeholder(size)


def get_metadata_info(request: HttpRequest, cover_url: str) -> list[ImageAsset]:
    """Returns media artwork details."""
    return [
        ImageAsset(
            src=request.build_absolute_uri(get_cover_image_url(cover_url, size)),
            sizes=f"{size}x{size}",
            type="image/webp",
        )
        for size in get_cover_image_sizes()
    ]
