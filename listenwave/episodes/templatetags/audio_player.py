from django import template
from django.template.context import RequestContext

from listenwave import covers
from listenwave.episodes.models import Episode

register = template.Library()


@register.simple_tag(takes_context=True)
def get_media_metadata(context: RequestContext, episode: Episode) -> dict:
    """Returns media session metadata for integration with client device.

    For more details:

        https://developers.google.com/web/updates/2017/02/media-session
    """

    return {
        "title": episode.cleaned_title,
        "album": episode.podcast.cleaned_title,
        "artist": episode.podcast.owner,
        "artwork": covers.get_metadata_info(
            context.request,
            episode.get_cover_url(),
        ),
    }


@register.inclusion_tag("episodes/_audio_player.html", takes_context=True)
def audio_player(context: RequestContext) -> dict:
    """Renders audio player if audio log in current session."""

    defaults = {
        "current_time": None,
        "episode": None,
        "is_playing": False,
        "start_player": False,
        "request": context.request,
    }
    if (
        context.request.user.is_authenticated
        and (episode_id := context.request.audio_player.get())
        and (
            audio_log := context.request.user.audio_logs.filter(episode__pk=episode_id)
            .select_related("episode", "episode__podcast")
            .first()
        )
    ):
        return defaults | {
            "episode": audio_log.episode,
            "current_time": audio_log.current_time,
            "is_playing": True,
        }

    return defaults
