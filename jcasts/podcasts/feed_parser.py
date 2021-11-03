from __future__ import annotations

import http
import multiprocessing
import secrets
import statistics
import traceback

from datetime import datetime, timedelta
from functools import lru_cache

import attr
import requests

from django.db import transaction
from django.utils import timezone
from django.utils.http import http_date, quote_etag
from django_rq import job

from jcasts.episodes.models import Episode
from jcasts.podcasts import date_parser, rss_parser, text_parser
from jcasts.podcasts.models import Category, Podcast

ACCEPT_HEADER = "application/atom+xml,application/rdf+xml,application/rss+xml,application/x-netcdf,application/xml;q=0.9,text/xml;q=0.2,*/*;q=0.1"

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
]


MIN_FREQUENCY = timedelta(hours=3)
MAX_FREQUENCY = timedelta(days=14)


class NotModified(requests.RequestException):
    ...


class DuplicateFeed(requests.RequestException):
    ...


@attr.s(kw_only=True)
class ParseResult:
    rss: str | None = attr.ib()
    success: bool = attr.ib(default=False)
    status: int | None = attr.ib(default=None)
    result: str | None = attr.ib(default=None)
    exception: Exception | None = attr.ib(default=None)

    def __bool__(self) -> bool:
        return self.success

    def raise_exception(self) -> None:
        if self.exception:
            raise self.exception


def reschedule(frequency: timedelta, pub_date: datetime | None) -> datetime:
    """Get the next scheduled datetime based on update frequency.

    By default, start from the latest pub date of the podcast and add the frequency.

    Keep incrementing by the frequency until we have scheduled time in the
    future.
    """
    now = timezone.now()
    pub_date = pub_date or now
    scheduled = pub_date + frequency

    while scheduled < now:
        scheduled += frequency

    return max(min(scheduled, now + MAX_FREQUENCY), now + MIN_FREQUENCY)


def calc_frequency(pub_dates: list[datetime]) -> timedelta:
    """Calculate the frequency based on avg interval between pub dates
    of individual episodes."""

    now = timezone.now()

    # assume max limit if no available dates or latest is out of range

    if not pub_dates or max(pub_dates) < now - MAX_FREQUENCY:
        return MAX_FREQUENCY

    # if just a single date, use current time as starting point

    if len(pub_dates) == 1:
        pub_dates = [now] + pub_dates

    first, *pub_dates = sorted(pub_dates, reverse=True)

    # calculate average distance between dates

    diffs: list[float] = []

    for pub_date in pub_dates:
        diffs.append((first - pub_date).total_seconds())
        first = pub_date

    # should fall inside min/max boundaries

    return max(
        min(timedelta(seconds=statistics.mean(diffs)), MAX_FREQUENCY), MIN_FREQUENCY
    )


def incr_frequency(frequency: timedelta | None, increment: float = 1.2) -> timedelta:
    """Increments the frequency by the provided amount. We should
    do this on each update 'miss'."""

    # should fall inside min/max boundaries

    return (
        min(timedelta(seconds=frequency.total_seconds() * increment), MAX_FREQUENCY)
        if frequency
        else MAX_FREQUENCY
    )


def parse_podcast_feeds(frequency: timedelta = timedelta(hours=1)) -> None:
    """
    Parses individual podcast feeds for update. This should include any
    podcast feeds already scheduled.
    """

    qs = (
        Podcast.objects.active()
        .with_followed()
        .scheduled()
        .distinct()
        .order_by(
            "scheduled",
            "-pub_date",
        )
    )

    # rough estimate: takes 2 seconds per update
    limit = multiprocessing.cpu_count() * round(frequency.total_seconds() / 2)

    podcast_ids = list(qs[:limit].values_list("pk", flat=True))

    Podcast.objects.filter(pk__in=podcast_ids).update(queued=timezone.now())

    for podcast_id in podcast_ids:
        parse_podcast_feed.delay(podcast_id)


@job("feeds")
@transaction.atomic
def parse_podcast_feed(podcast_id: int) -> ParseResult:

    try:
        podcast = Podcast.objects.get(pk=podcast_id, active=True)
        response = get_feed_response(podcast)
        feed, items = rss_parser.parse_rss(response.content)

        if not is_feed_changed(podcast, feed):
            raise NotModified(response=response)

        return parse_success(podcast, response, feed, items)

    except Podcast.DoesNotExist as e:
        return ParseResult(rss=None, success=False, exception=e)

    except NotModified as e:
        return parse_failure(
            podcast,
            status=e.response.status_code,
            result=Podcast.Result.NOT_MODIFIED,
        )

    except DuplicateFeed as e:
        return parse_failure(
            podcast,
            active=False,
            result=Podcast.Result.DUPLICATE_FEED,
            status=e.response.status_code,
        )

    except requests.HTTPError as e:
        return parse_failure(
            podcast,
            result=Podcast.Result.HTTP_ERROR,
            status=e.response.status_code,
            active=False,
        )

    except requests.RequestException as e:
        return parse_failure(
            podcast,
            exception=e,
            result=Podcast.Result.NETWORK_ERROR,
            tb=traceback.format_exc(),
        )

    except rss_parser.RssParserError as e:
        return parse_failure(
            podcast,
            result=Podcast.Result.INVALID_RSS,
            status=response.status_code,
            active=False,
            exception=e,
            tb=traceback.format_exc(),
        )


def get_feed_response(podcast: Podcast) -> requests.Response:
    response = requests.get(
        podcast.rss,
        headers=get_feed_headers(podcast),
        allow_redirects=True,
        timeout=10,
    )

    response.raise_for_status()

    if response.status_code == http.HTTPStatus.NOT_MODIFIED:
        raise NotModified(response=response)

    if (
        response.url != podcast.rss
        and Podcast.objects.filter(rss=response.url).exists()
    ):
        raise DuplicateFeed(response=response)

    return response


def parse_success(
    podcast: Podcast,
    response: requests.Response,
    feed: rss_parser.Feed,
    items: list[rss_parser.Item],
) -> ParseResult:

    # feed status
    podcast.rss = response.url
    podcast.http_status = response.status_code
    podcast.etag = response.headers.get("ETag", "")
    podcast.modified = date_parser.parse_date(response.headers.get("Last-Modified"))

    now = timezone.now()

    podcast.polled = now
    podcast.queued = None
    podcast.active = True
    podcast.result = Podcast.Result.SUCCESS  # type: ignore
    podcast.exception = ""

    # parsing status
    pub_dates = [item.pub_date for item in items if item.pub_date]

    podcast.pub_date = max(pub_dates)
    podcast.frequency = calc_frequency(pub_dates)
    podcast.scheduled = reschedule(podcast.frequency, podcast.pub_date)

    # content

    for field in (
        "cover_url",
        "description",
        "explicit",
        "funding_text",
        "funding_url",
        "language",
        "last_build_date",
        "link",
        "owner",
        "title",
    ):
        setattr(podcast, field, getattr(feed, field))

    # taxonomy
    categories_dct = get_categories_dict()

    categories = [
        categories_dct[category]
        for category in feed.categories
        if category in categories_dct
    ]
    podcast.keywords = " ".join(
        category for category in feed.categories if category not in categories_dct
    )
    podcast.extracted_text = extract_text(podcast, categories, items)

    podcast.categories.set(categories)  # type: ignore

    podcast.save()

    # episodes
    parse_episodes(podcast, items)

    return ParseResult(rss=podcast.rss, success=True, status=response.status_code)


def parse_episodes(
    podcast: Podcast, items: list[rss_parser.Item], batch_size: int = 500
) -> None:
    """Remove any episodes no longer in feed, update any current and
    add new"""

    qs = Episode.objects.filter(podcast=podcast)

    # remove any episodes that may have been deleted on the podcast
    qs.exclude(guid__in=[item.guid for item in items]).delete()

    # determine new/current items
    guids = dict(qs.values_list("guid", "pk"))

    episodes = [
        Episode(pk=guids.get(item.guid), podcast=podcast, **attr.asdict(item))
        for item in items
    ]

    # update existing content

    Episode.objects.bulk_update(
        [episode for episode in episodes if episode.guid in guids],
        fields=[
            "cover_url",
            "description",
            "duration",
            "episode",
            "episode_type",
            "explicit",
            "keywords",
            "length",
            "media_type",
            "media_url",
            "pub_date",
            "season",
            "title",
        ],
        batch_size=batch_size,
    )

    # new episodes

    Episode.objects.bulk_create(
        [episode for episode in episodes if episode.guid not in guids],
        ignore_conflicts=True,
        batch_size=batch_size,
    )


def extract_text(
    podcast: Podcast, categories: list[Category], items: list[rss_parser.Item]
) -> str:
    text = " ".join(
        value
        for value in [
            podcast.title,
            podcast.description,
            podcast.keywords,
            podcast.owner,
        ]
        + [c.name for c in categories]
        + [item.title for item in items][:6]
        if value
    )
    return " ".join(text_parser.extract_keywords(podcast.language, text))


def get_feed_headers(podcast: Podcast) -> dict[str, str]:
    headers = {
        "Accept": ACCEPT_HEADER,
        "User-Agent": secrets.choice(USER_AGENTS),
    }

    if podcast.etag:
        headers["If-None-Match"] = quote_etag(podcast.etag)
    if podcast.modified:
        headers["If-Modified-Since"] = http_date(podcast.modified.timestamp())
    return headers


def is_feed_changed(podcast: Podcast, feed: rss_parser.Feed) -> bool:
    return (
        None in (podcast.last_build_date, feed.last_build_date)
        or podcast.last_build_date != feed.last_build_date
    )


@lru_cache
def get_categories_dict() -> dict[str, Category]:
    return Category.objects.in_bulk(field_name="name")


def parse_failure(
    podcast: Podcast,
    *,
    status: int | None = None,
    active: bool = True,
    result: tuple[str, str] | None = None,
    exception: Exception | None = None,
    tb: str = "",
) -> ParseResult:

    now = timezone.now()

    frequency = incr_frequency(podcast.frequency)

    Podcast.objects.filter(pk=podcast.id).update(
        active=active,
        updated=now,
        polled=now,
        frequency=frequency,
        scheduled=reschedule(frequency, podcast.pub_date),
        result=result,
        http_status=status,
        exception=tb,
        queued=None,
    )

    return ParseResult(
        rss=podcast.rss,
        success=False,
        status=status,
        result=result[0] if result else None,
        exception=exception,
    )
