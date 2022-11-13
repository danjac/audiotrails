from __future__ import annotations

import datetime

from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.utils import timezone
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.http import require_POST, require_safe

static_page = require_safe(render)

_cache_control = cache_control(max_age=settings.DEFAULT_CACHE_TIMEOUT, immutable=True)
_cache_page = cache_page(settings.DEFAULT_CACHE_TIMEOUT)


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
        (settings.BASE_DIR / "radiofeed" / "static" / "img" / "wave-ico.png").open("rb")
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
    return JsonResponse(
        {
            "background_color": "#ffffff",
            "description": "Podcast aggregator site",
            "dir": "ltr",
            "display": "standalone",
            "name": "radiofeed",
            "orientation": "any",
            "scope": "/",
            "short_name": "Radiofeed",
            "start_url": "/",
            "theme_color": "#ffffff",
            "categories": ["podcasts"],
            "screenshots": [
                static("img/desktop.png"),
                static("img/mobile.png"),
            ],
            "icons": [
                {
                    "src": static("img/wave.png"),
                    "type": "image/png",
                    "purpose": "any",
                    "sizes": "512x512",
                },
                {
                    "src": static("img/favicon.png"),
                    "type": "image/png",
                    "sizes": "512x512",
                },
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
