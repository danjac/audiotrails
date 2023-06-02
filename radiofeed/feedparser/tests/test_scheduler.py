from datetime import timedelta

import pytest
from django.utils import timezone

from radiofeed.feedparser import scheduler
from radiofeed.feedparser.factories import create_feed, create_item
from radiofeed.feedparser.models import Feed, Item
from radiofeed.podcasts.factories import create_podcast
from radiofeed.podcasts.models import Podcast


class TestNextScheduledUpdate:
    def test_pub_date_none(self):
        now = timezone.now()
        podcast = Podcast(parsed=now - timedelta(hours=3), pub_date=None)
        assert (scheduler.next_scheduled_update(podcast) - now).total_seconds() < 10

    def test_parsed_none(self):
        now = timezone.now()
        podcast = Podcast(pub_date=now - timedelta(hours=3), parsed=None)
        assert (scheduler.next_scheduled_update(podcast) - now).total_seconds() < 10

    def test_parsed_gt_max(self):
        now = timezone.now()
        podcast = Podcast(
            pub_date=now - timedelta(days=5),
            parsed=now - timedelta(days=3),
            frequency=timedelta(days=30),
        )
        assert (scheduler.next_scheduled_update(podcast) - now).days == 4

    def test_parsed_lt_now(self):
        now = timezone.now()
        podcast = Podcast(
            pub_date=now - timedelta(days=5),
            parsed=now - timedelta(days=16),
            frequency=timedelta(days=30),
        )
        assert (scheduler.next_scheduled_update(podcast) - now).total_seconds() < 10

    def test_pub_date_lt_now(self):
        now = timezone.now()
        podcast = Podcast(
            pub_date=now - timedelta(days=33),
            parsed=now - timedelta(days=3),
            frequency=timedelta(days=30),
        )
        assert (scheduler.next_scheduled_update(podcast) - now).total_seconds() < 10

    def test_pub_date_in_future(self):
        now = timezone.now()
        podcast = Podcast(
            pub_date=now - timedelta(days=5),
            parsed=now - timedelta(hours=12),
            frequency=timedelta(days=7),
        )
        assert (scheduler.next_scheduled_update(podcast) - now).days == 2

    def test_pub_date_lt_min(self):
        now = timezone.now()
        podcast = Podcast(
            pub_date=now - timedelta(hours=3),
            parsed=now - timedelta(minutes=30),
            frequency=timedelta(hours=3),
        )
        assert (
            scheduler.next_scheduled_update(podcast) - now
        ).total_seconds() / 3600 == pytest.approx(0.5)


class TestGetPodcastsForUpdate:
    @pytest.mark.parametrize(
        (
            "active",
            "parsed",
            "pub_date",
            "frequency",
            "websub_mode",
            "websub_expires",
            "podping",
            "queued",
            "exists",
        ),
        [
            (
                True,
                None,
                None,
                timedelta(hours=24),
                "",
                None,
                False,
                False,
                True,
            ),
            (
                False,
                None,
                None,
                timedelta(hours=24),
                "",
                None,
                False,
                False,
                False,
            ),
            (
                True,
                timedelta(seconds=1200),
                timedelta(days=3),
                timedelta(hours=24),
                "",
                None,
                False,
                False,
                False,
            ),
            (
                True,
                timedelta(hours=3),
                timedelta(days=3),
                timedelta(hours=24),
                "",
                None,
                False,
                False,
                True,
            ),
            (
                True,
                timedelta(days=3),
                timedelta(days=3),
                timedelta(hours=24),
                "",
                None,
                False,
                False,
                True,
            ),
            (
                False,
                timedelta(days=3),
                timedelta(days=3),
                timedelta(hours=24),
                "",
                None,
                False,
                False,
                False,
            ),
            (
                True,
                timedelta(hours=3),
                timedelta(hours=3),
                timedelta(hours=24),
                "",
                None,
                False,
                False,
                False,
            ),
            (
                True,
                timedelta(hours=3),
                timedelta(hours=3),
                timedelta(hours=24),
                "",
                None,
                False,
                True,
                False,
            ),
            (
                True,
                timedelta(days=15),
                timedelta(days=15),
                timedelta(days=30),
                "",
                None,
                False,
                False,
                True,
            ),
            (
                True,
                timedelta(days=30),
                timedelta(days=90),
                timedelta(days=30),
                "",
                None,
                False,
                False,
                True,
            ),
            (
                True,
                timedelta(days=30),
                timedelta(days=90),
                timedelta(days=30),
                "",
                None,
                True,
                False,
                False,
            ),
            (
                True,
                timedelta(days=30),
                timedelta(days=90),
                timedelta(days=30),
                "",
                None,
                True,
                True,
                True,
            ),
            (
                True,
                timedelta(days=30),
                timedelta(days=90),
                timedelta(days=30),
                "subscribe",
                None,
                False,
                False,
                True,
            ),
            (
                True,
                timedelta(days=30),
                timedelta(days=90),
                timedelta(days=30),
                "subscribe",
                timedelta(days=-3),
                False,
                False,
                True,
            ),
            (
                True,
                timedelta(days=30),
                timedelta(days=90),
                timedelta(days=30),
                "subscribe",
                timedelta(days=3),
                False,
                False,
                False,
            ),
            (
                True,
                timedelta(days=30),
                timedelta(days=90),
                timedelta(days=30),
                "subscribe",
                timedelta(days=3),
                False,
                True,
                True,
            ),
            (
                False,
                timedelta(days=30),
                timedelta(days=90),
                timedelta(days=30),
                "subscribe",
                timedelta(days=3),
                False,
                True,
                False,
            ),
        ],
    )
    @pytest.mark.django_db
    def test_get_podcasts_for_update(
        self,
        active,
        parsed,
        pub_date,
        frequency,
        websub_mode,
        websub_expires,
        podping,
        queued,
        exists,
    ):
        now = timezone.now()
        create_podcast(
            active=active,
            parsed=now - parsed if parsed else None,
            pub_date=now - pub_date if pub_date else None,
            websub_expires=now + websub_expires if websub_expires else None,
            websub_mode=websub_mode,
            frequency=frequency,
            podping=podping,
            queued=now if queued else None,
        )

        assert scheduler.get_podcasts_for_update().exists() == exists


class TestReschedule:
    def test_pub_date_none(self):
        assert scheduler.reschedule(None, timedelta(hours=24)).days == 1

    def test_reschedule_no_change(self):
        assert scheduler.reschedule(timezone.now(), timedelta(days=10)).days == 10

    def test_increment(self):
        assert scheduler.reschedule(
            timezone.now() - timedelta(days=1), timedelta(hours=24)
        ).total_seconds() / 3600 == pytest.approx(24.24)


class TestSchedule:
    def test_single_date(self):
        feed = Feed(
            **create_feed(),
            items=[
                Item(
                    **create_item(
                        pub_date=timezone.now() - timedelta(days=3),
                    )
                )
            ],
        )

        assert scheduler.schedule(feed).days == 3

    def test_single_date_rescheduled(self):
        feed = Feed(
            **create_feed(),
            items=[
                Item(
                    **create_item(
                        pub_date=timezone.now() - timedelta(days=33),
                    )
                )
            ],
        )

        assert scheduler.schedule(feed).days == 33

    def test_median_empty(self):
        pub_date = timezone.now() - timedelta(days=3)

        items = [Item(**create_item(pub_date=pub_date)) for _ in range(12)]

        feed = Feed(**create_feed(), items=items)

        assert scheduler.schedule(feed).days == 3

    def test_no_outliers(self):
        items = []
        last = timezone.now()

        for day in [7] * 12:
            pub_date = last - timedelta(days=day)
            items.append(Item(**create_item(pub_date=pub_date)))
            last = pub_date

        feed = Feed(**create_feed(), items=items)

        assert scheduler.schedule(feed).days == pytest.approx(7)

    def test_variation(self):
        items = []
        last = timezone.now()

        for day in [4, 3, 4, 2, 5, 2, 4, 4, 3, 4, 4, 4, 6, 5, 7, 7, 7, 7, 3]:
            pub_date = last - timedelta(days=day)
            items.append(Item(**create_item(pub_date=pub_date)))
            last = pub_date

        feed = Feed(**create_feed(), items=items)

        assert scheduler.schedule(feed).days == pytest.approx(4)

    def test_regular_pattern(self):
        items = []
        last = timezone.now()

        for day in [3, 4] * 12:
            pub_date = last - timedelta(days=day)
            items.append(Item(**create_item(pub_date=pub_date)))
            last = pub_date

        feed = Feed(**create_feed(), items=items)

        assert scheduler.schedule(feed).days == pytest.approx(3)

    def test_min_frequency(self):
        now = timezone.now()
        feed = Feed(
            **create_feed(),
            items=[
                Item(
                    **create_item(
                        pub_date=pub_date,
                    )
                )
                for pub_date in [
                    now - timedelta(seconds=1200 * i) for i in range(1, 12)
                ]
            ],
        )

        assert (scheduler.schedule(feed).total_seconds() / 3600) == pytest.approx(1)

    def test_rescheduled(self):
        now = timezone.now()
        feed = Feed(
            **create_feed(),
            items=[
                Item(
                    **create_item(
                        pub_date=pub_date,
                    )
                )
                for pub_date in [now - timedelta(days=33 * i) for i in range(1, 12)]
            ],
        )

        assert scheduler.schedule(feed).days == 33
