import contextlib
from concurrent.futures import wait

import djclick as click
from django.db.models import Count, F, QuerySet

from radiofeed.feedparser import feed_parser, scheduler
from radiofeed.feedparser.exceptions import FeedParserError
from radiofeed.http_client import Client, get_client
from radiofeed.podcasts.models import Podcast
from radiofeed.thread_pool import DatabaseSafeThreadPoolExecutor


@click.command()
@click.option("--limit", type=int, default=360, help="Number of feeds to process")
def command(limit: int) -> None:
    "Parses RSS feeds of all scheduled podcasts."

    client = get_client()

    with DatabaseSafeThreadPoolExecutor() as executor:
        wait(
            executor.db_safe_map(
                lambda podcast: _parse_feed(podcast, client),
                _get_scheduled_podcasts(limit),
            )
        )


def _get_scheduled_podcasts(limit: int) -> QuerySet[Podcast]:
    return (
        scheduler.get_scheduled_podcasts()
        .alias(subscribers=Count("subscriptions"))
        .filter(active=True)
        .order_by(
            F("subscribers").desc(),
            F("promoted").desc(),
            F("parsed").asc(nulls_first=True),
        )[:limit]
    )


def _parse_feed(podcast: Podcast, client: Client) -> None:
    with contextlib.suppress(FeedParserError):
        feed_parser.parse_feed(podcast, client)
