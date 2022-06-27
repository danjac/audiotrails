from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from ratelimit.decorators import ratelimit

from radiofeed.common.decorators import ajax_login_required
from radiofeed.common.http import HttpResponseConflict, HttpResponseNoContent
from radiofeed.common.pagination import pagination_response
from radiofeed.episodes.models import AudioLog, Bookmark, Episode
from radiofeed.podcasts.models import Podcast


@require_http_methods(["GET"])
def index(request):

    promoted = "promoted" in request.GET
    since = timezone.now() - timedelta(days=14)

    subscribed = (
        set(request.user.subscription_set.values_list("podcast", flat=True))
        if request.user.is_authenticated
        else set()
    )

    podcasts = Podcast.objects.filter(pub_date__gt=since)

    if subscribed and not promoted:
        podcasts = podcasts.filter(pk__in=subscribed)
    else:
        podcasts = podcasts.filter(promoted=True)

    episodes = (
        Episode.objects.filter(pub_date__gt=since)
        .select_related("podcast")
        .filter(
            podcast__in=set(podcasts.values_list("pk", flat=True)),
        )
        .order_by("-pub_date", "-id")
        .distinct()
    )

    return pagination_response(
        request,
        episodes,
        "episodes/index.html",
        "episodes/pagination/episodes.html",
        {
            "promoted": promoted,
            "has_subscriptions": bool(subscribed),
            "search_url": reverse("episodes:search_episodes"),
        },
    )


@require_http_methods(["GET"])
def search_episodes(request):

    if not request.search:
        return HttpResponseRedirect(reverse("episodes:index"))

    episodes = (
        Episode.objects.select_related("podcast")
        .search(request.search.value)
        .order_by("-rank", "-pub_date")
    )

    return pagination_response(
        request,
        episodes,
        "episodes/search.html",
        "episodes/pagination/episodes.html",
    )


@require_http_methods(["GET"])
def episode_detail(request, episode_id, slug: str | None = None):
    episode = get_episode_or_404(
        request, episode_id, with_podcast=True, with_current_time=True
    )
    return TemplateResponse(
        request,
        "episodes/detail.html",
        {
            "episode": episode,
            "is_playing": request.player.has(episode.id),
            "is_bookmarked": episode.is_bookmarked(request.user),
            "next_episode": Episode.objects.get_next_episode(episode),
            "previous_episode": Episode.objects.get_previous_episode(episode),
        },
    )


@require_http_methods(["POST"])
@ajax_login_required
def start_player(request, episode_id):
    episode = get_episode_or_404(request, episode_id, with_podcast=True)

    log, _ = AudioLog.objects.update_or_create(
        episode=episode,
        user=request.user,
        defaults={
            "listened": timezone.now(),
        },
    )

    request.player.set(episode.id)

    return render_player(
        request,
        episode,
        start_player=True,
        current_time=log.current_time,
        listened=log.listened,
    )


@require_http_methods(["POST"])
@ajax_login_required
def close_player(request):

    if episode_id := request.player.pop():

        episode = get_episode_or_404(request, episode_id, with_current_time=True)

        return render_player(
            request,
            episode,
            start_player=False,
            current_time=episode.current_time,
            listened=episode.listened,
        )

    return HttpResponse()


@ratelimit(key="ip", rate="20/m")
@require_http_methods(["POST"])
@ajax_login_required
def player_time_update(request):
    """Update current play time of episode."""

    if episode_id := request.player.get():
        try:

            AudioLog.objects.filter(episode=episode_id, user=request.user).update(
                current_time=int(request.POST["current_time"]),
                listened=timezone.now(),
            )

        except (KeyError, ValueError):
            return HttpResponseBadRequest()

    return HttpResponseNoContent()


@require_http_methods(["GET"])
@login_required
def history(request):

    newest_first = request.GET.get("ordering", "desc") == "desc"

    logs = AudioLog.objects.filter(user=request.user).select_related(
        "episode", "episode__podcast"
    )

    if request.search:
        logs = logs.search(request.search.value).order_by("-rank", "-listened")
    else:
        logs = logs.order_by("-listened" if newest_first else "listened")

    return pagination_response(
        request,
        logs,
        "episodes/history.html",
        "episodes/pagination/history.html",
        {
            "newest_first": newest_first,
            "oldest_first": not (newest_first),
        },
    )


@require_http_methods(["DELETE"])
@ajax_login_required
def remove_audio_log(request, episode_id):

    episode = get_episode_or_404(request, episode_id)

    if not request.player.has(episode.id):
        AudioLog.objects.filter(user=request.user, episode=episode).delete()
        messages.info(request, "Removed from History")

    return TemplateResponse(
        request,
        "episodes/buttons/history.html",
        {"episode": episode},
    )


@require_http_methods(["GET"])
@login_required
def bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related(
        "episode", "episode__podcast"
    )
    if request.search:
        bookmarks = bookmarks.search(request.search.value).order_by("-rank", "-created")

    else:
        bookmarks = bookmarks.order_by("-created")
    return pagination_response(
        request,
        bookmarks,
        "episodes/bookmarks.html",
        "episodes/pagination/bookmarks.html",
    )


@require_http_methods(["POST"])
@ajax_login_required
def add_bookmark(request, episode_id):
    episode = get_episode_or_404(request, episode_id)

    try:
        Bookmark.objects.create(episode=episode, user=request.user)
    except IntegrityError:
        return HttpResponseConflict()

    messages.success(request, "Added to Bookmarks")

    return render_bookmark_buttons(request, episode, True)


@require_http_methods(["DELETE"])
@ajax_login_required
def remove_bookmark(request, episode_id):
    episode = get_episode_or_404(request, episode_id)

    Bookmark.objects.filter(user=request.user, episode=episode).delete()

    messages.info(request, "Removed from Bookmarks")

    return render_bookmark_buttons(request, episode, False)


def get_episode_or_404(
    request, episode_id, *, with_podcast=False, with_current_time=False
):
    qs = Episode.objects.all()
    if with_podcast:
        qs = qs.select_related("podcast")
    if with_current_time:
        qs = qs.with_current_time(request.user)
    return get_object_or_404(qs, pk=episode_id)


def render_player(
    request,
    episode: Episode,
    *,
    start_player,
    current_time,
    listened,
):
    return TemplateResponse(
        request,
        "episodes/player.html",
        {
            "episode": episode,
            "start_player": start_player,
            "is_playing": start_player,
            "current_time": current_time,
            "listened": listened,
        },
    )


def render_bookmark_buttons(request, episode, is_bookmarked):
    return TemplateResponse(
        request,
        "episodes/buttons/bookmark.html",
        {
            "episode": episode,
            "is_bookmarked": is_bookmarked,
        },
    )
