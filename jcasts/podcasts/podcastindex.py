import base64
import hashlib
import time

from datetime import timedelta
from functools import lru_cache
from typing import Optional

import attr
import requests

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils import timezone

from jcasts.podcasts.feed_parser import parse_feed
from jcasts.podcasts.models import Podcast
from jcasts.podcasts.rss_parser import validate_url


def search(search_term):
    return with_podcasts(
        parse_feed_data(get_client().fetch("/search/byterm", {"q": search_term}))
    )


def search_cached(search_term):

    cache_key = (
        "podcastindex:" + base64.urlsafe_b64encode(bytes(search_term, "utf-8")).hex()
    )
    if (feeds := cache.get(cache_key)) is not None:
        return feeds

    feeds = search(search_term)
    cache.set(cache_key, feeds)
    return feeds


def new_feeds(limit=20, since=timedelta(hours=24)):

    return with_podcasts(
        parse_feed_data(
            get_client().fetch(
                "/recent/newfeeds",
                {
                    "max": limit,
                    "since": (timezone.now() - since).timestamp(),
                },
            )
        )
    )


@lru_cache
def get_client():
    return Client.from_settings()


def parse_feed_data(data):
    def _parse_feed(result):
        try:
            return Feed(
                **{k: v for k, v in result.items() if k in ("url", "title", "image")}
            )
        except (TypeError, ValueError, ValidationError) as e:
            print(e)
            return None

    return [
        feed
        for feed in [_parse_feed(result) for result in data.get("feeds", [])]
        if feed
    ]


def with_podcasts(feeds):
    """Looks up podcast associated with result. Adds new podcasts if they are not already in the database"""

    podcasts = Podcast.objects.filter(rss__in=[f.url for f in feeds]).in_bulk(
        field_name="rss"
    )

    new_podcasts = []

    for feed in feeds:
        feed.podcast = podcasts.get(feed.url, None)
        if feed.podcast is None:
            new_podcasts.append(Podcast(title=feed.title, rss=feed.url))

    if new_podcasts:
        Podcast.objects.bulk_create(new_podcasts, ignore_conflicts=True)

        for podcast in new_podcasts:
            parse_feed.delay(podcast.rss, force_update=True)

    return feeds


@attr.s
class Feed:
    url: str = attr.ib(validator=validate_url)
    title: str = attr.ib(default="")
    image: str = attr.ib(default="")

    podcast: Optional[Podcast] = None


class Client:
    base_url = "https://api.podcastindex.org/api/1.0"
    user_agent = "Voyce"

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    @classmethod
    def from_settings(cls):

        config = getattr(settings, "PODCASTINDEX_CONFIG", {})

        api_key = config.setdefault("api_key", None)
        api_secret = config.setdefault("api_secret", None)

        if None in (api_key, api_secret):
            raise ValueError("API Key and API Secret must be set in settings")

        return cls(api_key, api_secret)

    def fetch(self, endpoint, data=None):
        response = requests.post(
            self.base_url + endpoint, headers=self.get_headers(), data=data
        )
        response.raise_for_status()
        return response.json()

    def get_headers(self):

        epoch_time = int(time.time())

        hashed = self.api_key + self.api_secret + str(epoch_time)

        sha_1 = hashlib.sha1(hashed.encode()).hexdigest()  # nosec

        return {
            "X-Auth-Date": str(epoch_time),
            "X-Auth-Key": self.api_key,
            "Authorization": sha_1,
            "User-Agent": self.user_agent,
        }
