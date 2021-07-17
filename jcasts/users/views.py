import csv
import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views.decorators.http import (
    require_http_methods,
    require_POST,
    require_safe,
)

from jcasts.episodes.models import AudioLog, Favorite, QueueItem
from jcasts.podcasts.models import Follow, Podcast
from jcasts.users.forms import UserPreferencesForm


@require_http_methods(["GET", "POST"])
@login_required
def user_preferences(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserPreferencesForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your preferences have been saved")
            return redirect(request.path)
    else:
        form = UserPreferencesForm(instance=request.user)

    return TemplateResponse(request, "account/preferences.html", {"form": form})


@require_http_methods(["GET", "POST"])
@login_required
def export_podcast_feeds(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return TemplateResponse(request, "account/export_podcast_feeds.html")
    # set a max limit of 500 for now to prevent a DOS attack
    podcasts = (
        Podcast.objects.filter(follow__user=request.user, pub_date__isnull=False)
        .distinct()
        .order_by("-pub_date")
    )[:500]

    filename = f"podcasts-{timezone.now().strftime('%Y-%m-%d')}"

    if request.POST.get("format") == "opml":
        response = TemplateResponse(
            request,
            "account/opml.xml",
            {"podcasts": podcasts},
            content_type="application/xml",
        )
        response["Content-Disposition"] = f"attachment; filename={filename}.xml"
        return response

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={filename}.csv"
    writer = csv.writer(response)
    writer.writerow(["Title", "RSS", "Website", "Published"])
    for podcast in podcasts:
        writer.writerow(
            [
                podcast.title,
                podcast.rss,
                podcast.link,
                podcast.pub_date.strftime("%Y-%m-%d"),
            ]
        )
    return response


@require_safe
@login_required
def user_stats(request: HttpRequest) -> HttpResponse:

    logs = AudioLog.objects.filter(user=request.user)

    return TemplateResponse(
        request,
        "account/stats.html",
        {
            "stats": {
                "listened": logs.count(),
                "in_progress": logs.filter(completed__isnull=True).count(),
                "completed": logs.filter(completed__isnull=False).count(),
                "follows": Follow.objects.filter(user=request.user).count(),
                "in_queue": QueueItem.objects.filter(user=request.user).count(),
                "favorites": Favorite.objects.filter(user=request.user).count(),
            },
        },
    )


@require_http_methods(["GET", "POST"])
@login_required
def delete_account(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and "confirm-delete" in request.POST:
        request.user.delete()
        logout(request)
        messages.info(request, "Your account has been deleted")
        return redirect(settings.HOME_URL)
    return TemplateResponse(request, "account/delete_account.html")


@require_POST
def accept_cookies(request: HttpRequest) -> HttpResponse:
    response = HttpResponse()
    response.set_cookie(
        "accept-cookies",
        value="true",
        expires=timezone.now() + datetime.timedelta(days=30),
        secure=False,
        httponly=False,
        samesite="Lax",
    )
    return response
