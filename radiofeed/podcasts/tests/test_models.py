from __future__ import annotations

import pytest

from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.utils.translation import override

from radiofeed.common.factories import create_batch
from radiofeed.podcasts.factories import (
    create_category,
    create_podcast,
    create_recommendation,
)
from radiofeed.podcasts.models import Category, Podcast, Recommendation
from radiofeed.users.factories import create_user


class TestRecommendationManager:
    def test_bulk_delete(self, db):
        create_batch(create_recommendation, 3)
        Recommendation.objects.bulk_delete()
        assert Recommendation.objects.count() == 0


class TestCategoryManager:
    @pytest.fixture
    def category(self, db):
        return create_category(name="testing", name_fi="testaaminen")

    def test_search_empty(self, category):
        assert Category.objects.search("").count() == 0

    def test_search_english(self, category):

        with override("en"):
            assert Category.objects.search("testing").count() == 1
            assert Category.objects.search("testaaminen").count() == 0

    def test_search_finnish(self, category):

        with override("fi"):
            assert Category.objects.search("testing").count() == 0
            assert Category.objects.search("testaaminen").count() == 1


class TestCategoryModel:
    def test_slug(self):
        category = Category(name="Testing")
        assert category.slug == "testing"

    def test_str(self):
        category = Category(name="Testing")
        assert str(category) == "Testing"


class TestPodcastManager:
    def test_search(self, db):
        create_podcast(title="testing")
        assert Podcast.objects.search("testing").count() == 1

    def test_search_if_empty(self, db):
        create_podcast(title="testing")
        assert Podcast.objects.search("").count() == 0


class TestPodcastModel:
    def test_str(self):
        assert str(Podcast(title="title")) == "title"

    def test_str_title_empty(self):
        rss = "https://example.com/rss.xml"
        assert str(Podcast(title="", rss=rss)) == rss

    def test_slug(self):
        assert Podcast(title="Testing").slug == "testing"

    def test_slug_if_title_empty(self):
        assert Podcast().slug == "no-title"

    def test_cleaned_title(self):
        podcast = Podcast(title="<b>Test &amp; Code")
        assert podcast.cleaned_title == "Test & Code"

    def test_cleaned_description(self):
        podcast = Podcast(description="<b>Test &amp; Code")
        assert podcast.cleaned_description == "Test & Code"

    def test_is_subscribed_anonymous(self, podcast):
        assert not podcast.is_subscribed(AnonymousUser())

    def test_is_subscribed_false(self, podcast):
        assert not podcast.is_subscribed(create_user())

    def test_is_subscribed_true(self, subscription):
        assert subscription.podcast.is_subscribed(subscription.subscriber)

    def test_get_latest_episode_url(self, podcast):
        url = podcast.get_latest_episode_url()
        assert url == reverse(
            "podcasts:latest_episode", args=[podcast.id, podcast.slug]
        )

    def test_get_subscribe_target(self):
        return Podcast(id=12345).get_subscribe_target() == "subscribe-actions-12345"
