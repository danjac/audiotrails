from unittest import mock

import pytest

from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest

from jcasts.podcasts.admin import (
    ActiveFilter,
    PodcastAdmin,
    PromotedFilter,
    PubDateFilter,
)
from jcasts.podcasts.factories import PodcastFactory
from jcasts.podcasts.models import Podcast


class TestPodcastAdmin:
    @pytest.fixture(scope="class")
    def admin(self) -> PodcastAdmin:
        return PodcastAdmin(Podcast, AdminSite())

    @pytest.fixture
    def podcasts(self, db) -> list[Podcast]:
        return PodcastFactory.create_batch(3, active=True, promoted=False)

    @pytest.fixture
    def req(self, rf) -> HttpRequest:
        req = rf.get("/")
        req._messages = mock.Mock()
        return req

    def test_source(self, podcasts, admin):
        podcast = podcasts[0]
        assert admin.source(podcasts[0]) == podcast.get_domain()

    def test_get_search_results(self, podcasts, admin, req):
        podcast = PodcastFactory(title="Indie Hackers")
        qs, _ = admin.get_search_results(req, Podcast.objects.all(), "Indie Hackers")
        assert qs.count() == 1
        assert qs.first() == podcast

    def test_get_search_results_no_search_term(self, podcasts, admin, req):
        qs, _ = admin.get_search_results(req, Podcast.objects.all(), "")
        assert qs.count() == 3

    def test_reactivate(self, podcasts, admin, req):
        PodcastFactory(active=False, error_status=404)
        admin.reactivate(req, Podcast.objects.all())
        assert Podcast.objects.filter(error_status=None, active=True).count() == 4

    def test_sync_podcast_feeds(self, podcast, admin, req, mocker):
        mock_task = mocker.patch("jcasts.podcasts.tasks.sync_podcast_feed.delay")
        admin.sync_podcast_feeds(req, Podcast.objects.all())
        mock_task.assert_called_with(podcast.id, force_update=True)

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
