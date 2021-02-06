import http
import json
from typing import Dict, List, Optional

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max, OuterRef, QuerySet, Subquery
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_POST

from turbo_response import TurboFrame, TurboStream, TurboStreamResponse

from radiofeed.pagination import paginate
from radiofeed.podcasts.models import Podcast
from radiofeed.users.decorators import ajax_login_required

from .models import AudioLog, Episode, Favorite, QueueItem


@login_required
def episode_list(request: HttpRequest) -> HttpResponse:

    subscriptions: List[int] = (
        list(request.user.subscription_set.values_list("podcast", flat=True))
        if request.user.is_authenticated
        else []
    )
    has_subscriptions: bool = bool(subscriptions)

    if has_subscriptions:
        # we want a list of the *latest* episode for each podcast
        latest_episodes = (
            Episode.objects.filter(podcast=OuterRef("pk"))
            .order_by("-pub_date")
            .distinct()
        )

        episode_ids = (
            Podcast.objects.filter(pk__in=subscriptions)
            .annotate(latest_episode=Subquery(latest_episodes.values("pk")[:1]))
            .values_list("latest_episode", flat=True)
            .distinct()
        )

        episodes = (
            Episode.objects.select_related("podcast")
            .filter(pk__in=set(episode_ids))
            .order_by("-pub_date")
            .distinct()
        )
    else:
        episodes = Episode.objects.none()

    return episode_list_response(
        request,
        episodes,
        "episodes/index.html",
        {"has_subscriptions": has_subscriptions},
    )


def search_episodes(request: HttpRequest) -> HttpResponse:

    if request.search:
        episodes = (
            Episode.objects.select_related("podcast")
            .search(request.search)
            .order_by("-rank", "-pub_date")
        )
        return episode_list_response(request, episodes, "episodes/search.html")

    if request.user.is_authenticated:
        return redirect("episodes:episode_list")

    return redirect("podcasts:podcast_list")


def episode_detail(
    request: HttpRequest, episode_id: int, slug: Optional[str] = None
) -> HttpResponse:
    episode = get_object_or_404(
        Episode.objects.with_current_time(request.user).select_related("podcast"),
        pk=episode_id,
    )
    return TemplateResponse(
        request,
        "episodes/detail.html",
        {
            "episode": episode,
            "is_favorited": is_episode_favorited(request, episode),
            "is_queued": is_episode_queued(request, episode),
            "og_data": get_episode_opengraph_data(request, episode),
        },
    )


@login_required
def episode_actions(
    request: HttpRequest,
    episode_id: str,
    allow_favorites: bool = True,
    allow_queue: bool = True,
) -> HttpResponse:
    episode = get_object_or_404(
        Episode.objects.with_current_time(request.user).select_related("podcast"),
        pk=episode_id,
    )

    if request.turbo.frame:
        return (
            TurboFrame(request.turbo.frame)
            .template(
                "episodes/_actions.html",
                {
                    "episode": episode,
                    "player_toggle_id": f"episode-play-actions-toggle-{episode.id}",
                    "is_episode_playing": request.player.is_playing(episode),
                    "is_favorited": allow_favorites
                    and is_episode_favorited(request, episode),
                    "is_queued": allow_queue and is_episode_queued(request, episode),
                    "allow_favorites": allow_favorites,
                    "allow_queue": allow_queue,
                },
            )
            .response(request)
        )

    return redirect(episode.get_absolute_url())


@login_required
def history(request: HttpRequest) -> HttpResponse:

    logs = (
        AudioLog.objects.filter(user=request.user)
        .select_related("episode", "episode__podcast")
        .order_by("-updated")
    )

    if request.search:
        logs = logs.search(request.search).order_by("-rank", "-updated")
    else:
        logs = logs.order_by("-updated")

    context = {
        "page_obj": paginate(request, logs),
    }
    if request.turbo.frame:

        return (
            TurboFrame(request.turbo.frame)
            .template("episodes/history/_episode_list.html", context)
            .response(request)
        )

    return TemplateResponse(request, "episodes/history/index.html", context)


@require_POST
@login_required
def remove_history(request: HttpRequest, episode_id: int) -> HttpResponse:

    episode = get_object_or_404(Episode, pk=episode_id)
    AudioLog.objects.filter(user=request.user, episode=episode).delete()

    if request.turbo:
        return TurboStream(f"episode-{episode.id}").remove.response()
    return redirect("episodes:history")


@login_required
def favorite_list(request: HttpRequest) -> HttpResponse:
    favorites = Favorite.objects.filter(user=request.user).select_related(
        "episode", "episode__podcast"
    )
    if request.search:
        favorites = favorites.search(request.search).order_by("-rank", "-created")
    else:
        favorites = favorites.order_by("-created")

    context: Dict = {
        "page_obj": paginate(request, favorites),
    }

    if request.turbo.frame:

        return (
            TurboFrame(request.turbo.frame)
            .template("episodes/favorites/_episode_list.html", context)
            .response(request)
        )

    return TemplateResponse(request, "episodes/favorites/index.html", context)


@require_POST
@login_required
def add_favorite(request: HttpRequest, episode_id: int) -> HttpResponse:
    episode = get_object_or_404(Episode, pk=episode_id)

    try:
        Favorite.objects.create(episode=episode, user=request.user)
    except IntegrityError:
        pass
    return episode_favorite_response(request, episode, True)


@require_POST
@login_required
def remove_favorite(request: HttpRequest, episode_id: int) -> HttpResponse:
    episode = get_object_or_404(Episode, pk=episode_id)
    Favorite.objects.filter(user=request.user, episode=episode).delete()
    if "remove" in request.POST:
        return TurboStream(f"episode-{episode.id}").remove.response()
    return episode_favorite_response(request, episode, False)


# Queue views


@login_required
def queue(request: HttpRequest) -> HttpResponse:
    # we don't want to paginate the queue
    return TemplateResponse(
        request,
        "episodes/queue/index.html",
        {
            "queue_items": QueueItem.objects.filter(user=request.user)
            .select_related("episode", "episode__podcast")
            .order_by("position")
        },
    )


@require_POST
@login_required
def add_to_queue(request: HttpRequest, episode_id: int) -> HttpResponse:
    episode = get_object_or_404(Episode, pk=episode_id)
    position = (
        QueueItem.objects.filter(user=request.user).aggregate(Max("position"))[
            "position__max"
        ]
        or 0
    ) + 1

    try:
        QueueItem.objects.create(user=request.user, episode=episode, position=position)
    except IntegrityError:
        pass

    # NB: we probably don't want to add the "queue" button in the Queue itself
    return episode_queue_response(request, episode, True)


@require_POST
@login_required
def remove_from_queue(request: HttpRequest, episode_id: int) -> HttpResponse:
    episode = get_object_or_404(Episode, pk=episode_id)
    QueueItem.objects.filter(user=request.user, episode=episode).delete()
    if "remove" in request.POST:
        return TurboStreamResponse(render_remove_from_queue(request, episode))
    return episode_queue_response(request, episode, False)


@require_POST
@ajax_login_required
def move_queue_items(request: HttpRequest) -> HttpResponse:

    qs = QueueItem.objects.filter(user=request.user)
    items = qs.in_bulk()
    for_update = []

    try:
        for position, item_id in enumerate(request.POST.getlist("items"), 1):
            if item := items[int(item_id)]:
                item.position = position
                for_update.append(item)
    except (KeyError, ValueError):
        return HttpResponseBadRequest("Invalid payload")

    qs.bulk_update(for_update, ["position"])
    return HttpResponse(status=http.HTTPStatus.NO_CONTENT)


# Player control views


@require_POST
@login_required
def toggle_player(
    request: HttpRequest, episode_id: Optional[int] = None, action: str = "play"
) -> HttpResponse:
    """Add episode to session and returns HTML component. The player info
    is then added to the session."""

    streams: List[str] = []

    # clear session
    if current_episode := request.player.eject():
        streams += render_player_toggles(request, current_episode, False)

        if request.POST.get("mark_complete") == "true":
            current_episode.log_activity(request.user, current_time=0, completed=True)

    if action == "stop":
        return player_stop_response(streams)

    if action == "next":

        if next_item := (
            QueueItem.objects.filter(user=request.user)
            .select_related("episode")
            .order_by("position")
            .first()
        ):

            episode = next_item.episode
            current_time = 0
            next_item.delete()

        else:
            return player_stop_response(streams)

    else:

        if episode_id is None:
            raise Http404()

        episode = get_object_or_404(
            Episode.objects.with_current_time(request.user).select_related("podcast"),
            pk=episode_id,
        )

        # remove from queue
        QueueItem.objects.filter(user=request.user, episode=episode).delete()
        current_time = 0 if episode.completed else episode.current_time or 0

    episode.log_activity(request.user, current_time=current_time)

    request.player.start(episode, current_time)

    response = TurboStreamResponse(
        streams
        + render_remove_from_queue(request, episode)
        + render_player_toggles(request, episode, True)
        + [
            TurboStream("player-container")
            .update.template(
                "episodes/player/_player.html", {"episode": episode}, request=request
            )
            .render(),
        ]
    )
    response["X-Player"] = json.dumps(
        {
            "action": "start",
            "mediaUrl": episode.media_url,
            "currentTime": current_time,
            "metadata": episode.get_media_metadata(),
        }
    )
    return response


@require_POST
@ajax_login_required
def player_timeupdate(request: HttpRequest) -> HttpResponse:
    """Update current play time of episode"""

    if episode := request.player.get_episode():
        try:
            current_time = round(float(request.POST["current_time"]))
        except KeyError:
            return HttpResponseBadRequest("current_time not provided")
        except ValueError:
            return HttpResponseBadRequest("current_time invalid")

        try:
            playback_rate = float(request.POST["playback_rate"])
        except (KeyError, ValueError):
            playback_rate = 1.0

        episode.log_activity(request.user, current_time)
        request.player.current_time = current_time
        request.player.playback_rate = playback_rate

        return HttpResponse(status=http.HTTPStatus.NO_CONTENT)
    return HttpResponseBadRequest("No player loaded")


def episode_list_response(
    request: HttpRequest,
    episodes: QuerySet,
    template_name: str,
    extra_context: Optional[Dict] = None,
) -> HttpResponse:
    context = {
        "page_obj": paginate(request, episodes),
        "search_url": reverse("episodes:search_episodes"),
        **(extra_context or {}),
    }
    if request.turbo.frame:

        return (
            TurboFrame(request.turbo.frame)
            .template("episodes/_episode_list.html", context)
            .response(request)
        )

    return TemplateResponse(request, template_name, context)


def render_player_toggles(
    request: HttpRequest, episode: Episode, is_playing: bool
) -> List[str]:

    return [
        TurboStream(target)
        .replace.template(
            "episodes/player/_toggle.html",
            {
                "episode": episode,
                "is_episode_playing": is_playing,
                "player_toggle_id": target,
            },
            request=request,
        )
        .render()
        for target in [
            f"episode-play-toggle-{episode.id}",
            f"episode-play-actions-toggle-{episode.id}",
        ]
    ]


def render_remove_from_queue(request: HttpRequest, episode: Episode) -> List[str]:
    streams = [TurboStream(f"queue-item-{episode.id}").remove.render()]
    if QueueItem.objects.filter(user=request.user).count() == 0:
        streams += [
            TurboStream("queue").append.render("No more items left in queue"),
        ]
    return streams


def player_stop_response(streams: List[str]) -> HttpResponse:
    response = TurboStreamResponse(
        streams + [TurboStream("player-controls").remove.render()]
    )
    response["X-Player"] = json.dumps({"action": "stop"})
    return response


def episode_favorite_response(
    request: HttpRequest, episode: Episode, is_favorited: bool
) -> HttpResponse:
    if request.turbo:
        # https://github.com/hotwired/turbo/issues/86
        return (
            TurboFrame(episode.get_favorite_toggle_id())
            .template(
                "episodes/favorites/_toggle.html",
                {"episode": episode, "is_favorited": is_favorited},
            )
            .response(request)
        )
    return redirect(episode)


def episode_queue_response(
    request: HttpRequest, episode: Episode, is_queued: bool
) -> HttpResponse:
    if request.turbo:
        # https://github.com/hotwired/turbo/issues/86
        return (
            TurboFrame(episode.get_queue_toggle_id())
            .template(
                "episodes/queue/_toggle.html",
                {"episode": episode, "is_queued": is_queued},
            )
            .response(request)
        )
    return redirect(episode)


def get_episode_opengraph_data(
    request: HttpRequest, episode: Episode
) -> Dict[str, str]:
    og_data: Dict = {
        "url": request.build_absolute_uri(episode.get_absolute_url()),
        "title": f"{request.site.name} | {episode.podcast.title} | {episode.title}",
        "description": episode.description,
    }

    if episode.podcast.cover_image:
        og_data |= {
            "image": episode.podcast.cover_image.url,
            "image_height": episode.podcast.cover_image.height,
            "image_width": episode.podcast.cover_image.width,
        }

    return og_data


def is_episode_queued(request: HttpRequest, episode: Episode) -> bool:
    if request.user.is_anonymous:
        return False
    return QueueItem.objects.filter(episode=episode, user=request.user).exists()


def is_episode_favorited(request: HttpRequest, episode: Episode) -> bool:
    if request.user.is_anonymous:
        return False
    return Favorite.objects.filter(episode=episode, user=request.user).exists()
