from __future__ import annotations

import statistics

from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone

from jcasts.episodes.models import Episode
from jcasts.podcasts.models import Podcast

MIN_FREQ = timedelta(hours=1)
MAX_FREQ = timedelta(days=7)


def schedule_podcast_feeds() -> int:
    """Sets podcast feed scheduled times. This can be run once to set
    initial scheduling, afterwards should be calibrated automatically after fresh
    pull attempts.
    """

    qs = Podcast.objects.filter(active=True, pub_date__isnull=False).order_by(
        "-pub_date"
    )

    for_update = []

    for podcast in qs.iterator():
        podcast.scheduled = schedule(podcast)
        for_update.append(podcast)

    Podcast.objects.bulk_update(for_update, fields=["scheduled"], batch_size=1000)

    return len(for_update)


def get_frequency(pub_dates: list[datetime]) -> timedelta | None:
    """Calculates frequency given set of pub dates. If no available dates within range,
    returns None.
    """
    now = timezone.now()

    min_date = now - settings.RELEVANCY_THRESHOLD

    pub_dates = [
        pub_date for pub_date in sorted(pub_dates, reverse=True) if pub_date > min_date
    ]

    # we need at least 3 dates for meaningful comparison

    if len(pub_dates) < 3:
        return None

    (head, *tail) = pub_dates

    diffs = []

    for pub_date in tail:
        diffs.append((head - pub_date).total_seconds())
        head = pub_date

    freq = timedelta(seconds=round(statistics.mean(diffs)))

    # min 1 hour, max 7 days
    return min(max(freq, MIN_FREQ), MAX_FREQ)


def get_recent_pub_dates(podcast: Podcast) -> list[datetime]:
    return (
        Episode.objects.filter(
            podcast=podcast, pub_date__gte=timezone.now() - settings.RELEVANCY_THRESHOLD
        )
        .values_list("pub_date", flat=True)
        .order_by("-pub_date")
    )


def schedule(
    podcast: Podcast,
    pub_dates: list[datetime] | None = None,
) -> datetime | None:
    """Returns next scheduled feed sync time.
    Will calculate based on list of provided pub dates or most recent episodes.
    """
    if not podcast.active or podcast.pub_date is None:
        return None

    now = timezone.now()

    freq = get_frequency(pub_dates or get_recent_pub_dates(podcast))

    if freq and (scheduled := podcast.pub_date + freq) > now:
        return scheduled

    # add 5% of freq to current time (min 1 hour)
    # e.g. 7 days - try again in about 8 hours

    diff = timedelta(seconds=(now - podcast.pub_date).total_seconds() * 0.05)

    return now + max(diff, MIN_FREQ)
