# Standard Library
import json

# Django
from django.urls import reverse

# Third Party Libraries
import pytest

# RadioFeed
from radiofeed.episodes.factories import EpisodeFactory

# Local
from .. import views
from ..factories import CategoryFactory, PodcastFactory, SubscriptionFactory
from ..itunes import SearchResult
from ..models import Podcast, Subscription

pytestmark = pytest.mark.django_db


class TestPodcastList:
    def test_anonymous(self, rf, anonymous_user):
        PodcastFactory.create_batch(3)
        req = rf.get(reverse("podcasts:podcast_list"))
        req.user = anonymous_user
        resp = views.podcast_list(req)
        assert resp.status_code == 200
        assert len(resp.context_data["podcasts"]) == 3

    def test_user_no_subscriptions(self, rf, user):
        """If user has no subscriptions, just show general feed"""
        PodcastFactory.create_batch(3)
        req = rf.get(reverse("podcasts:podcast_list"))
        req.user = user
        resp = views.podcast_list(req)
        assert resp.status_code == 200
        assert len(resp.context_data["podcasts"]) == 3

    def test_user_has_subscriptions(self, rf, user):
        """If user has subscriptions, show only own feed"""
        PodcastFactory.create_batch(3)
        sub = SubscriptionFactory(user=user)
        req = rf.get(reverse("podcasts:podcast_list"))
        req.user = user
        resp = views.podcast_list(req)
        assert resp.status_code == 200
        assert len(resp.context_data["podcasts"]) == 1
        assert resp.context_data["podcasts"][0] == sub.podcast

    def test_search_anonymous(self, rf, anonymous_user):
        PodcastFactory.create_batch(3, title="zzz", keywords="zzzz")
        req = rf.get(reverse("podcasts:podcast_list"), {"q": "testing"})
        req.user = anonymous_user
        podcast = PodcastFactory(title="testing")
        resp = views.podcast_list(req)
        assert resp.status_code == 200
        assert len(resp.context_data["podcasts"]) == 1
        assert resp.context_data["podcasts"][0] == podcast

    def test_search_has_subcription(self, rf, user):
        """Ignore subscribed feeds in search"""
        PodcastFactory.create_batch(3, title="zzzz", keywords="zzzz")
        SubscriptionFactory(user=user)
        req = rf.get(reverse("podcasts:podcast_list"), {"q": "testing"})
        req.user = user
        podcast = PodcastFactory(title="testing")
        resp = views.podcast_list(req)
        assert resp.status_code == 200
        assert len(resp.context_data["podcasts"]) == 1
        assert resp.context_data["podcasts"][0] == podcast


class TestPodcastDetail:
    def test_anonymous(self, rf, anonymous_user, podcast):
        EpisodeFactory.create_batch(3, podcast=podcast)
        req = rf.get(podcast.get_absolute_url())
        req.user = anonymous_user
        resp = views.podcast_detail(req, podcast.id, podcast.slug)
        assert resp.status_code == 200
        assert resp.context_data["podcast"] == podcast
        assert len(resp.context_data["episodes"]) == 3
        assert not resp.context_data["is_subscribed"]

    def test_search(self, rf, anonymous_user, podcast):
        EpisodeFactory.create_batch(3, podcast=podcast, title="zzzz", keywords="zzzz")
        EpisodeFactory(title="testing", podcast=podcast)
        req = rf.get(podcast.get_absolute_url(), {"q": "testing"})
        req.user = anonymous_user
        resp = views.podcast_detail(req, podcast.id, podcast.slug,)
        assert resp.status_code == 200
        assert resp.context_data["podcast"] == podcast
        assert len(resp.context_data["episodes"]) == 1


class TestAddPodcast:
    def test_add_podcast(self, rf, admin_user, mocker):
        data = {
            "itunes": "http://itunes.apple.com",
            "rss": "https://example.com/rss.xml",
            "title": "Example",
        }

        mock = mocker.patch("radiofeed.podcasts.views.sync_podcast_feed.delay")

        req = rf.post(
            reverse("podcasts:add_podcast"),
            json.dumps(data),
            content_type="application/json",
        )
        req.user = admin_user
        resp = views.add_podcast(req)

        podcast = Podcast.objects.get()
        assert podcast.title == data["title"]
        assert podcast.rss == data["rss"]
        assert podcast.itunes == data["itunes"]

        data = json.loads(resp.content)

        assert data["id"] == podcast.id

        mock.asset_called()


class TestCategoryList:
    def test_get(self, rf):
        parents = CategoryFactory.create_batch(3, parent=None)
        c1 = CategoryFactory(parent=parents[0])
        c2 = CategoryFactory(parent=parents[1])
        c3 = CategoryFactory(parent=parents[2])

        PodcastFactory(categories=[c1, parents[0]])
        PodcastFactory(categories=[c2, parents[1]])
        PodcastFactory(categories=[c3, parents[2]])

        resp = views.category_list(rf.get(reverse("podcasts:category_list")))
        assert resp.status_code == 200
        assert len(resp.context_data["categories"]) == 3

    def test_search(self, rf):
        parents = CategoryFactory.create_batch(3, parent=None)
        c1 = CategoryFactory(parent=parents[0])
        c2 = CategoryFactory(parent=parents[1])
        c3 = CategoryFactory(parent=parents[2], name="testing child")

        c4 = CategoryFactory(name="testing parent")

        PodcastFactory(categories=[c1])
        PodcastFactory(categories=[c2])
        PodcastFactory(categories=[c3])
        PodcastFactory(categories=[c4])

        resp = views.category_list(
            rf.get(reverse("podcasts:category_list"), {"q": "testing"})
        )
        assert resp.status_code == 200
        assert len(resp.context_data["categories"]) == 2
        assert resp.context_data["search"] == "testing"


class TestCategoryDetail:
    def test_get(self, rf, category):

        CategoryFactory.create_batch(3, parent=category)
        PodcastFactory.create_batch(12, categories=[category])

        resp = views.category_detail(
            rf.get(category.get_absolute_url()), category.id, category.slug
        )
        assert resp.status_code == 200
        assert resp.context_data["category"] == category
        assert len(resp.context_data["podcasts"]) == 12

    def test_search(self, rf, category):

        CategoryFactory.create_batch(3, parent=category)
        PodcastFactory.create_batch(
            12, title="zzzz", keywords="zzzz", categories=[category]
        )
        PodcastFactory(title="testing", categories=[category])

        req = rf.get(category.get_absolute_url(), {"q": "testing"})
        resp = views.category_detail(req, category.id, category.slug)

        assert resp.status_code == 200
        assert resp.context_data["category"] == category
        assert len(resp.context_data["podcasts"]) == 1
        assert resp.context_data["search"] == "testing"


class TestSubscribe:
    def test_subscribe(self, rf, podcast, user, mocker):
        req = rf.post(reverse("podcasts:subscribe", args=[podcast.id]))
        req.user = user
        req._messages = mocker.Mock()
        resp = views.subscribe(req, podcast.id)
        assert resp.url == podcast.get_absolute_url()
        req._messages.add.assert_called()

    def test_already_subscribed(self, rf, podcast, user, mocker):
        SubscriptionFactory(user=user, podcast=podcast)
        req = rf.post(reverse("podcasts:subscribe", args=[podcast.id]))
        req.user = user
        req._messages = mocker.Mock()
        resp = views.subscribe(req, podcast.id)
        assert resp.url == podcast.get_absolute_url()
        req._messages.add.assert_not_called()


class TestUnsubscribe:
    def test_unsubscribe(self, rf, podcast, user, mocker):
        SubscriptionFactory(user=user, podcast=podcast)
        req = rf.post(reverse("podcasts:unsubscribe", args=[podcast.id]))
        req.user = user
        req._messages = mocker.Mock()
        resp = views.unsubscribe(req, podcast.id)
        assert resp.url == podcast.get_absolute_url()
        req._messages.add.assert_called()
        assert not Subscription.objects.filter(podcast=podcast, user=user).exists()


class TestSearchITunes:
    def test_search(self, rf, mocker):
        def mock_search_itunes(search_term, num_results=12):
            return [
                SearchResult(
                    rss="http://example.com/test.xml",
                    itunes="https://apple.com/some-link",
                    image="test.jpg",
                    title="test title",
                )
            ]

        mocker.patch.object(views.itunes, "search_itunes", mock_search_itunes)
        req = rf.get(reverse("podcasts:search_itunes"), {"q": "test"})
        resp = views.search_itunes(req)

        assert resp.status_code == 200
        assert len(resp.context_data["results"]) == 1
        assert resp.context_data["results"][0].title == "test title"
