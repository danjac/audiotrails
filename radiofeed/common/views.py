from __future__ import annotations

import datetime
import io

import requests
import user_agent

from django.conf import settings
from django.http import (
    FileResponse,
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.http import require_POST, require_safe
from PIL import Image

_cache_control = cache_control(max_age=settings.DEFAULT_CACHE_TIMEOUT, immutable=True)
_cache_page = cache_page(settings.DEFAULT_CACHE_TIMEOUT)


@require_safe
def static_page(
    request: HttpRequest, template_name: str, extra_context: dict | None = None
) -> HttpResponse:
    """Renders simple static page."""
    return render(request, template_name, extra_context)


@require_POST
def accept_cookies(request: HttpRequest) -> HttpResponse:
    """Handles "accept" action on GDPR cookie banner."""
    response = HttpResponse()
    response.set_cookie(
        "accept-cookies",
        value="true",
        expires=timezone.now() + datetime.timedelta(days=365),
        secure=True,
        httponly=True,
        samesite="Lax",
    )
    return response


@require_safe
@_cache_control
def favicon(request: HttpRequest) -> FileResponse:
    """Generates favicon file."""
    return FileResponse(
        (settings.BASE_DIR / "static" / "img" / "wave-ico.png").open("rb")
    )


@require_safe
@_cache_control
@_cache_page
def service_worker(request: HttpRequest) -> HttpResponse:
    """PWA service worker."""
    return render(request, "service_worker.js", content_type="application/javascript")


@require_safe
@_cache_control
@_cache_page
def manifest(request: HttpRequest) -> HttpResponse:
    """PWA manifest.json file."""
    start_url = reverse("podcasts:landing_page")
    theme_color = "#26323C"

    icon = {
        "src": static("img/wave.png"),
        "type": "image/png",
        "sizes": "512x512",
    }

    return JsonResponse(
        {
            "background_color": theme_color,
            "theme_color": theme_color,
            "description": "Podcast aggregator site",
            "dir": "ltr",
            "display": "standalone",
            "name": "Radiofeed",
            "short_name": "Radiofeed",
            "orientation": "any",
            "scope": start_url,
            "start_url": start_url,
            "categories": [
                "books",
                "education",
                "entertainment",
                "news",
                "politics",
                "sport",
            ],
            "screenshots": [
                static("img/desktop.png"),
                static("img/mobile.png"),
            ],
            "icons": [
                icon,
                {**icon, "purpose": "any"},
                {**icon, "purpose": "maskable"},
            ],
            "shortcuts": [],
            "lang": "en",
        }
    )


@require_safe
@_cache_control
@_cache_page
def robots(request: HttpRequest) -> HttpResponse:
    """Generates robots.txt file."""
    return HttpResponse(
        "\n".join(
            [
                "User-Agent: *",
                *[
                    f"Disallow: {url}"
                    for url in [
                        "/account/",
                        "/bookmarks/",
                        "/categories/",
                        "/episodes/",
                        "/history/",
                        "/podcasts/",
                    ]
                ],
            ]
        ),
        content_type="text/plain",
    )


@require_safe
@_cache_control
@_cache_page
def security(request: HttpRequest) -> HttpResponse:
    """Generates security.txt file containing contact details etc."""
    return HttpResponse(
        "\n".join(
            [
                f"Contact: mailto:{settings.CONTACT_EMAIL}",
            ]
        ),
        content_type="text/plain",
    )


@require_safe
@_cache_control
def cover_image(request: HttpRequest, size: int, encoded_url: str) -> HttpResponse:
    """Proxies a cover image from remote source."""
    try:
        response = requests.get(
            urlsafe_base64_decode(encoded_url),
            headers={
                "User-Agent": user_agent.generate_user_agent(),
            },
        )
        response.raise_for_status()

        image = Image.open(io.BytesIO(response.content))
        image = image.resize((size, size), Image.ANTIALIAS)

        output = io.BytesIO()
        image.save(output, format="PNG")

    except (IOError, ValueError, requests.HTTPError):
        return HttpResponseBadRequest("Error: unable to download or process image")

    return HttpResponse(output.getvalue(), content_type="image/png")
