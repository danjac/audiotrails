from datetime import timedelta

import pytest
import pytz

from django.utils import timezone

from jcasts.episodes.factories import EpisodeFactory
from jcasts.podcasts import scheduler
from jcasts.podcasts.factories import PodcastFactory
from jcasts.podcasts.models import Podcast


class TestGetFrequency:
    def test_get_frequency(self):

        now = timezone.now()

        dates = [
            now - timedelta(days=5, hours=12),
            now - timedelta(days=12, hours=12),
            now - timedelta(days=15, hours=12),
            now - timedelta(days=30, hours=12),
        ]

        assert scheduler.get_frequency(dates).days == 6

    def test_get_frequency_single_date(self):

        assert (
            scheduler.get_frequency(
                [
                    timezone.now() - timedelta(days=5, hours=12),
                ]
            ).days
            == 5
        )

    def test_get_frequency_not_utc(self):

        dt = timezone.now() - timedelta(days=5, hours=12)
        dt = pytz.timezone("Europe/Helsinki").normalize(dt)

        assert scheduler.get_frequency([dt]).days == 5

    def test_get_frequency_if_empty(self):
        assert scheduler.get_frequency([]) is None


class TestSchedulePodcastFeeds:
    @pytest.mark.parametrize(
        "is_scheduled,last_pub,freq,active,result,num_scheduled",
        [
            (False, timedelta(days=30), timedelta(days=7), True, 1, 1),
            (True, timedelta(days=30), timedelta(days=7), True, 0, 1),
            (False, timedelta(days=30), None, True, 1, 0),
            (False, timedelta(days=99), timedelta(days=7), True, 0, 0),
            (False, None, timedelta(days=7), True, 0, 0),
        ],
    )
    def test_schedule(
        self, db, is_scheduled, last_pub, freq, active, result, num_scheduled
    ):
        now = timezone.now()

        podcast = PodcastFactory(
            scheduled=now if is_scheduled else None,
            pub_date=now - last_pub if last_pub else None,
            active=active,
        )

        if freq:
            EpisodeFactory(pub_date=now - freq, podcast=podcast)

        assert scheduler.schedule_podcast_feeds() == result
        assert Podcast.objects.filter(scheduled__isnull=False).count() == num_scheduled

    def test_schedule_reset(self, db):
        now = timezone.now()

        podcast = PodcastFactory(
            scheduled=now - timedelta(days=10),
            pub_date=now - timedelta(days=30),
            active=True,
        )

        EpisodeFactory(podcast=podcast, pub_date=timezone.now() - timedelta(days=3))

        scheduled = podcast.scheduled

        assert scheduler.schedule_podcast_feeds(reset=True) == 1
        assert Podcast.objects.filter(scheduled__isnull=False).count() == 1

        podcast.refresh_from_db()
        assert podcast.scheduled > scheduled


class TestSchedule:
    def test_schedule_no_pub_date(self, db):
        assert (
            scheduler.schedule(
                PodcastFactory(pub_date=None), self.get_pub_dates(3, 6, 9)
            )
            is None
        )

    def test_schedule_inactive(self, db):
        assert (
            scheduler.schedule(
                PodcastFactory(active=False), self.get_pub_dates(3, 6, 9)
            )
            is None
        )

    def test_schedule_frequency_zero(self, podcast):
        now = timezone.now()
        scheduled = scheduler.schedule(
            PodcastFactory(),
            [now - timedelta(hours=1)],
        )
        assert (scheduled - now).total_seconds() == pytest.approx(3600)

    def test_schedule_frequency_lt_one_hour(self, db):
        now = timezone.now()

        scheduled = scheduler.schedule(
            PodcastFactory(),
            [now - timedelta(minutes=30)],
        )
        assert (scheduled - now).total_seconds() == pytest.approx(3600, rel=10)

    def test_schedule_lt_now(self, db):
        now = timezone.now()
        scheduled = scheduler.schedule(PodcastFactory(), self.get_pub_dates(3, 6, 9))
        assert (scheduled - now).days == 2

    def test_schedule_from_episodes(self, podcast):
        now = timezone.now()

        [
            EpisodeFactory(podcast=podcast, pub_date=pub_date)
            for pub_date in self.get_pub_dates(3, 6, 9)
        ]
        scheduled = scheduler.schedule(podcast)
        assert (scheduled - now).total_seconds() / 3600 == pytest.approx(48)

    def get_pub_dates(self, *days):
        now = timezone.now()
        return [now - timedelta(days=day) for day in days]
