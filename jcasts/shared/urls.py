from django.urls import include, path

from jcasts.shared import views

about_urls = [
    path(
        "",
        views.static_page,
        name="credits",
        kwargs={"template_name": "about/credits.html"},
    ),
    path(
        "shortcuts/",
        views.static_page,
        name="shortcuts",
        kwargs={"template_name": "about/shortcuts.html"},
    ),
    path(
        "privacy/",
        views.static_page,
        name="privacy",
        kwargs={"template_name": "about/privacy.html"},
    ),
]

error_urls = [
    path(
        "400/",
        views.static_page,
        name="bad_request",
        kwargs={"template_name": "400.html"},
    ),
    path(
        "403/",
        views.static_page,
        name="forbidden",
        kwargs={"template_name": "403.html"},
    ),
    path(
        "404/",
        views.static_page,
        name="not_found",
        kwargs={"template_name": "404.html"},
    ),
    path(
        "405/",
        views.static_page,
        name="not_allowed",
        kwargs={"template_name": "405.html"},
    ),
    path(
        "500/",
        views.static_page,
        name="server_error",
        kwargs={"template_name": "500.html"},
    ),
    path(
        "csrf/",
        views.static_page,
        name="csrf",
        kwargs={"template_name": "403_csrf.html"},
    ),
]

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("robots.txt", views.robots, name="robots"),
    path("~accept_cookies", views.accept_cookies, name="accept_cookies"),
    path("about/", include((about_urls, "about"), namespace="about")),
    path("error/", include((error_urls, "error"), namespace="error")),
]
