from datetime import timedelta
from unittest import mock

import pytest

from django.contrib.admin.sites import AdminSite
from django.utils import timezone

from jcasts.podcasts.admin import (
    ActiveFilter,
    PodcastAdmin,
    PromotedFilter,
    PubDateFilter,
)
from jcasts.podcasts.factories import PodcastFactory
from jcasts.podcasts.models import Podcast


@pytest.fixture(scope="class")
def admin():
    return PodcastAdmin(Podcast, AdminSite())


@pytest.fixture
def podcasts(db):
    return PodcastFactory.create_batch(3, active=True, promoted=False)


@pytest.fixture
def req(rf):
    req = rf.get("/")
    req._messages = mock.Mock()
    return req


class TestPodcastAdmin:
    def test_source(self, podcasts, admin):
        assert admin.source(podcasts[0]) == podcasts[0].get_domain()

    def test_get_search_results(self, podcasts, admin, req):
        podcast = PodcastFactory(title="Indie Hackers")
        qs, _ = admin.get_search_results(req, Podcast.objects.all(), "Indie Hackers")
        assert qs.count() == 1
        assert qs.first() == podcast

    def test_get_search_results_no_search_term(self, podcasts, admin, req):
        qs, _ = admin.get_search_results(req, Podcast.objects.all(), "")
        assert qs.count() == 3

    def test_get_ordering_no_search_term(self, admin, req):
        ordering = admin.get_ordering(req)
        assert ordering == ["-parsed", "-pub_date"]

    def test_get_ordering_search_term(self, admin, req):
        req.GET = {"q": "test"}
        ordering = admin.get_ordering(req)
        assert ordering == []

    def test_parse_podcast_feeds(self, podcast, admin, req, mock_parse_podcast_feed):
        admin.parse_podcast_feeds(req, Podcast.objects.all())
        mock_parse_podcast_feed.assert_called_with(podcast.rss)

    def test_parse_podcast_feeds_inactive(
        self, podcast, admin, req, mock_parse_podcast_feed
    ):
        PodcastFactory(active=False)
        admin.parse_podcast_feeds(req, Podcast.objects.all())
        mock_parse_podcast_feed.assert_not_called()


class TestPubDateFilter:
    def test_pub_date_filter_none(self, podcasts, admin, req):
        PodcastFactory(pub_date=None)
        f = PubDateFilter(req, {}, Podcast, admin)
        qs = f.queryset(req, Podcast.objects.all())
        assert qs.count() == 4

    def test_pub_date_filter_false(self, podcasts, admin, req):
        no_pub_date = PodcastFactory(pub_date=None)
        f = PubDateFilter(req, {"pub_date": "no"}, Podcast, admin)
        qs = f.queryset(req, Podcast.objects.all())
        assert qs.count() == 1
        assert qs.first() == no_pub_date

    def test_pub_date_filter_true(self, podcasts, admin, req):
        no_pub_date = PodcastFactory(pub_date=None)
        f = PubDateFilter(req, {"pub_date": "yes"}, Podcast, admin)
        qs = f.queryset(req, Podcast.objects.all())
        assert qs.count() == 3
        assert no_pub_date not in qs

    def test_pub_date_stale(self, settings, podcasts, admin, req):
        now = timezone.now()
        settings.FRESHNESS_THRESHOLD = timedelta(days=90)
        PodcastFactory(pub_date=None)
        PodcastFactory(pub_date=now - timedelta(days=9))
        not_fresh = PodcastFactory(pub_date=now - timedelta(days=99))

        f = PubDateFilter(req, {"pub_date": "stale"}, Podcast, admin)
        qs = f.queryset(req, Podcast.objects.all())
        assert qs.count() == 1
        assert not_fresh in qs

    def test_pub_date_fresh(self, settings, podcasts, admin, req):
        now = timezone.now()
        settings.FRESHNESS_THRESHOLD = timedelta(days=90)
        no_pub_date = PodcastFactory(pub_date=None)
        not_fresh = PodcastFactory(pub_date=now - timedelta(days=99))

        f = PubDateFilter(req, {"pub_date": "fresh"}, Podcast, admin)
        qs = f.queryset(req, Podcast.objects.all())
        assert qs.count() == 4
        assert no_pub_date in qs
        assert not_fresh not in qs


class TestActiveFilter:
    def test_active_filter_none(self, podcasts, admin, req):
        PodcastFactory(active=False)
        f = ActiveFilter(req, {}, Podcast, admin)
        qs = f.queryset(req, Podcast.objects.all())
        assert qs.count() == 4

    def test_active_filter_false(self, podcasts, admin, req):
        inactive = PodcastFactory(active=False)
        f = ActiveFilter(req, {"active": "no"}, Podcast, admin)
        qs = f.queryset(req, Podcast.objects.all())
        assert qs.count() == 1
        assert qs.first() == inactive

    def test_active_filter_true(self, podcasts, admin, req):
        inactive = PodcastFactory(active=False)
        f = ActiveFilter(req, {"active": "yes"}, Podcast, admin)
        qs = f.queryset(req, Podcast.objects.all())
        assert qs.count() == 3
        assert inactive not in qs

    def test_promoted_filter_none(self, podcasts, admin, req):
        PodcastFactory(promoted=False)
        f = PromotedFilter(req, {}, Podcast, admin)
        qs = f.queryset(req, Podcast.objects.all())
        assert qs.count() == 4

    def test_promoted_filter_true(self, podcasts, admin, req):
        promoted = PodcastFactory(promoted=True)
        f = PromotedFilter(req, {"promoted": "yes"}, Podcast, admin)
        qs = f.queryset(req, Podcast.objects.all())
        assert qs.count() == 1
        assert qs.first() == promoted
