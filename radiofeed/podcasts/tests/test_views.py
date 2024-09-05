import pytest
from django.urls import reverse, reverse_lazy
from pytest_django.asserts import assertContains

from radiofeed.episodes.tests.factories import EpisodeFactory
from radiofeed.podcasts import itunes
from radiofeed.podcasts.models import Podcast, Subscription
from radiofeed.podcasts.tests.factories import (
    CategoryFactory,
    PodcastFactory,
    RecommendationFactory,
    SubscriptionFactory,
)
from radiofeed.tests.asserts import assert_200, assert_404, assert_409

_index_url = reverse_lazy("podcasts:index")
_subscriptions_url = reverse_lazy("podcasts:subscriptions")
_discover_url = reverse_lazy("podcasts:discover")


class TestIndex:
    @pytest.mark.django_db
    def test_anonymous(self, client):
        PodcastFactory.create_batch(3, promoted=True)
        assert_200(client.get(_index_url))

    @pytest.mark.django_db
    def test_authenticated(self, client, auth_user):
        response = client.get(_index_url)
        assert response.url == _subscriptions_url


class TestSubscriptions:
    @pytest.mark.django_db
    def test_authenticated_no_subscriptions(self, client, auth_user):
        PodcastFactory.create_batch(3, promoted=True)
        assert_200(client.get(_subscriptions_url))

    @pytest.mark.django_db
    def test_user_is_subscribed(self, client, auth_user):
        """If user subscribed any podcasts, show only own feed with these podcasts"""

        PodcastFactory.create_batch(3, promoted=True)
        sub = SubscriptionFactory(subscriber=auth_user)
        response = client.get(_subscriptions_url)

        assert_200(response)

        assert len(response.context["page_obj"].object_list) == 1
        assert response.context["page_obj"].object_list[0] == sub.podcast

    @pytest.mark.django_db
    def test_htmx_request(self, client, auth_user):
        PodcastFactory.create_batch(3, promoted=True)
        sub = SubscriptionFactory(subscriber=auth_user)
        response = client.get(
            _subscriptions_url,
            headers={
                "HX-Request": "true",
                "HX-Target": "pagination",
            },
        )

        assert_200(response)

        assert len(response.context["page_obj"].object_list) == 1
        assert response.context["page_obj"].object_list[0] == sub.podcast

    @pytest.mark.django_db
    def test_user_is_subscribed_search(self, client, auth_user):
        """If user subscribed any podcasts, show only own feed with these podcasts"""

        PodcastFactory.create_batch(3, promoted=True)
        sub = SubscriptionFactory(subscriber=auth_user)
        response = client.get(_subscriptions_url, {"search": sub.podcast.title})

        assert_200(response)

        assert len(response.context["page_obj"].object_list) == 1
        assert response.context["page_obj"].object_list[0] == sub.podcast


class TestDiscover:
    @pytest.mark.django_db
    def test_empty(self, client, auth_user):
        response = client.get(_discover_url)

        assert_200(response)

        assert len(response.context["page_obj"].object_list) == 0

    @pytest.mark.django_db
    def test_invalid_page(self, client, auth_user):
        assert_200(client.get(_discover_url, {"page": 1000}))

    @pytest.mark.django_db
    def test_next_page(self, client, auth_user):
        PodcastFactory.create_batch(33, promoted=True)
        response = client.get(_discover_url, {"page": 2})

        assert_200(response)

        assert len(response.context["page_obj"].object_list) == 3


class TestSearchPodcasts:
    url = reverse_lazy("podcasts:search_podcasts")

    @pytest.mark.django_db
    def test_search(self, client, auth_user, faker):
        podcast = PodcastFactory(title=faker.unique.text())
        PodcastFactory.create_batch(3, title="zzz", keywords="zzzz")
        response = client.get(self.url, {"search": podcast.title})

        assert_200(response)

        assert len(response.context["page_obj"].object_list) == 1
        assert response.context["page_obj"].object_list[0] == podcast

    @pytest.mark.django_db
    def test_search_value_empty(self, client, auth_user, faker):
        response = client.get(self.url, {"search": ""})
        assert response.url == _discover_url

    @pytest.mark.django_db
    def test_search_filter_private(self, client, auth_user, faker):
        podcast = PodcastFactory(title=faker.unique.text(), private=True)
        PodcastFactory.create_batch(3, title="zzz", keywords="zzzz")
        response = client.get(self.url, {"search": podcast.title})

        assert_200(response)

        assert len(response.context["page_obj"].object_list) == 0

    @pytest.mark.django_db
    def test_search_no_results(self, client, auth_user, faker):
        response = client.get(self.url, {"search": "zzzz"})
        assert_200(response)
        assert len(response.context["page_obj"].object_list) == 0


class TestSearchItunes:
    url = reverse_lazy("podcasts:search_itunes")

    @pytest.mark.django_db
    def test_empty(self, client, auth_user):
        response = client.get(self.url, {"search": ""})
        assert response.url == _discover_url

    @pytest.mark.django_db
    def test_search(self, client, auth_user, podcast, mocker):
        feeds = iter(
            [
                itunes.Feed(
                    url="https://example.com/id123456",
                    rss="https://feeds.fireside.fm/testandcode/rss",
                    title="Test & Code : Py4hon Testing",
                    image="https://assets.fireside.fm/file/fireside-images/podcasts/images/b/bc7f1faf-8aad-4135-bb12-83a8af679756/cover.jpg?v=3",
                ),
                itunes.Feed(
                    url=podcast.website,
                    rss=podcast.rss,
                    title=podcast.title,
                    image="https://assets.fireside.fm/file/fireside-images/podcasts/images/b/bc7f1faf-8aad-4135-bb12-83a8af679756/cover.jpg?v=3",
                    podcast=podcast,
                ),
            ]
        )
        mock_search = mocker.patch(
            "radiofeed.podcasts.itunes.search", return_value=feeds
        )

        assert_200(client.get(self.url, {"search": "test"}))

        mock_search.assert_called()


class TestPodcastSimilar:
    @pytest.mark.django_db
    def test_get(self, client, auth_user, podcast):
        EpisodeFactory.create_batch(3, podcast=podcast)
        RecommendationFactory.create_batch(3, podcast=podcast)
        response = client.get(podcast.get_similar_url())

        assert_200(response)

        assert response.context["podcast"] == podcast
        assert len(response.context["recommendations"]) == 3


class TestPodcastDetail:
    @pytest.fixture
    def podcast(self, faker):
        return PodcastFactory(
            owner=faker.name(),
            website=faker.url(),
            funding_url=faker.url(),
            funding_text=faker.text(),
            keywords=faker.text(),
            categories=CategoryFactory.create_batch(3),
        )

    @pytest.mark.django_db
    def test_get_podcast_no_website(self, client, auth_user, faker):
        podcast = PodcastFactory(website=None, owner=faker.name())
        response = client.get(podcast.get_absolute_url())

        assert_200(response)

        assert response.context["podcast"] == podcast

    @pytest.mark.django_db
    def test_get_podcast_subscribed(self, client, auth_user, podcast):
        podcast.categories.set(CategoryFactory.create_batch(3))
        SubscriptionFactory(subscriber=auth_user, podcast=podcast)
        response = client.get(podcast.get_absolute_url())

        assert_200(response)

        assert response.context["podcast"] == podcast
        assert response.context["is_subscribed"] is True

    @pytest.mark.django_db
    def test_get_podcast_private_subscribed(self, client, auth_user):
        podcast = PodcastFactory(private=True)
        SubscriptionFactory(subscriber=auth_user, podcast=podcast)
        response = client.get(podcast.get_absolute_url())

        assert_200(response)

        assert response.context["podcast"] == podcast
        assert response.context["is_subscribed"] is True

    @pytest.mark.django_db
    def test_get_podcast_private_not_subscribed(self, client, auth_user):
        podcast = PodcastFactory(private=True)
        response = client.get(podcast.get_absolute_url())

        assert_200(response)

        assert response.context["podcast"] == podcast
        assert response.context["is_subscribed"] is False

    @pytest.mark.django_db
    def test_get_podcast_not_subscribed(self, client, auth_user, podcast):
        response = client.get(podcast.get_absolute_url())

        assert_200(response)

        assert response.context["podcast"] == podcast
        assert response.context["is_subscribed"] is False

    @pytest.mark.django_db
    def test_get_podcast_admin(self, client, staff_user, podcast):
        response = client.get(podcast.get_absolute_url())

        assert_200(response)

        assert response.context["podcast"] == podcast
        assertContains(response, "Admin")


class TestLatestEpisode:
    @pytest.mark.django_db
    def test_ok(self, client, auth_user, episode):
        response = client.get(episode.podcast.get_latest_episode_url())
        assert response.url == episode.get_absolute_url()

    @pytest.mark.django_db
    def test_no_episodes(self, client, auth_user, podcast):
        assert_404(client.get(podcast.get_latest_episode_url()))


class TestPodcastEpisodes:
    @pytest.mark.django_db
    def test_get_episodes(self, client, auth_user, podcast):
        EpisodeFactory.create_batch(33, podcast=podcast)

        response = client.get(self.url(podcast))
        assert_200(response)

        assert len(response.context["page_obj"].object_list) == 30

    @pytest.mark.django_db
    def test_no_episodes(self, client, auth_user, podcast):
        response = client.get(self.url(podcast))

        assert_200(response)
        assert len(response.context["page_obj"].object_list) == 0

    @pytest.mark.django_db
    def test_ascending(self, client, auth_user, podcast):
        EpisodeFactory.create_batch(33, podcast=podcast)

        response = client.get(
            self.url(podcast),
            {"order": "asc"},
        )
        assert_200(response)

        assert len(response.context["page_obj"].object_list) == 30

    @pytest.mark.django_db
    def test_search(self, client, auth_user, podcast, faker):
        EpisodeFactory.create_batch(3, podcast=podcast)

        episode = EpisodeFactory(title=faker.unique.name(), podcast=podcast)

        response = client.get(
            self.url(podcast),
            {"search": episode.title},
        )
        assert_200(response)
        assert len(response.context["page_obj"].object_list) == 1

    def url(self, podcast):
        return podcast.get_episodes_url()


class TestCategoryList:
    url = reverse_lazy("podcasts:category_list")

    @pytest.mark.django_db
    def test_matching_podcasts(self, client, auth_user):
        for _ in range(3):
            category = CategoryFactory()
            category.podcasts.add(PodcastFactory())

        response = client.get(self.url)
        assert_200(response)
        assert len(response.context["categories"]) == 3

    @pytest.mark.django_db
    def test_no_matching_podcasts(
        self,
        client,
        auth_user,
    ):
        CategoryFactory.create_batch(3)
        response = client.get(self.url)
        assert_200(response)
        assert len(response.context["categories"]) == 0

    @pytest.mark.django_db
    def test_search(self, client, auth_user, category, faker):
        CategoryFactory.create_batch(3)

        category = CategoryFactory(name="testing")
        category.podcasts.add(PodcastFactory())

        response = client.get(self.url, {"search": "testing"})
        assert_200(response)
        assert len(response.context["categories"]) == 1

    @pytest.mark.django_db
    def test_search_no_matching_podcasts(self, client, auth_user, category, faker):
        CategoryFactory.create_batch(3)

        CategoryFactory(name="testing")

        response = client.get(self.url, {"search": "testing"})
        assert_200(response)
        assert len(response.context["categories"]) == 0


class TestCategoryDetail:
    @pytest.mark.django_db
    def test_get(self, client, auth_user, category):
        PodcastFactory.create_batch(12, categories=[category])
        response = client.get(category.get_absolute_url())
        assert_200(response)
        assert response.context["category"] == category

    @pytest.mark.django_db
    def test_search(self, client, auth_user, category, faker):
        PodcastFactory.create_batch(
            12, title="zzzz", keywords="zzzz", categories=[category]
        )
        podcast = PodcastFactory(title=faker.unique.text(), categories=[category])

        response = client.get(category.get_absolute_url(), {"search": podcast.title})
        assert_200(response)

        assert len(response.context["page_obj"].object_list) == 1

    @pytest.mark.django_db
    def test_no_podcasts(self, client, auth_user, category):
        response = client.get(category.get_absolute_url())
        assert_200(response)
        assert len(response.context["page_obj"].object_list) == 0


class TestSubscribe:
    def url(self, podcast):
        return reverse("podcasts:subscribe", args=[podcast.pk])

    @pytest.mark.django_db
    def test_subscribe(self, client, podcast, auth_user):
        response = client.post(
            self.url(podcast),
            headers={
                "HX-Request": "true",
            },
        )

        assert_200(response)

        assert Subscription.objects.filter(
            podcast=podcast, subscriber=auth_user
        ).exists()

    @pytest.mark.django_db
    def test_subscribe_private(self, client, auth_user):
        podcast = PodcastFactory(private=True)

        response = client.post(
            self.url(podcast),
            headers={
                "HX-Request": "true",
                "HX-Target": "subscribe-button",
            },
        )

        assert_404(response)

        assert not Subscription.objects.filter(
            podcast=podcast, subscriber=auth_user
        ).exists()

    @pytest.mark.django_db()(transaction=True)
    def test_already_subscribed(
        self,
        client,
        podcast,
        auth_user,
    ):
        SubscriptionFactory(subscriber=auth_user, podcast=podcast)
        assert_409(
            client.post(
                self.url(podcast),
                headers={
                    "HX-Request": "true",
                    "HX-Target": "subscribe-button",
                },
            )
        )

        assert Subscription.objects.filter(
            podcast=podcast, subscriber=auth_user
        ).exists()


class TestUnsubscribe:
    def url(self, podcast):
        return reverse("podcasts:unsubscribe", args=[podcast.pk])

    @pytest.mark.django_db
    def test_unsubscribe(self, client, auth_user, podcast):
        SubscriptionFactory(subscriber=auth_user, podcast=podcast)
        response = client.delete(
            self.url(podcast),
            headers={
                "HX-Request": "true",
                "HX-Target": "subscribe-button",
            },
        )

        assert_200(response)

        assert not Subscription.objects.filter(
            podcast=podcast, subscriber=auth_user
        ).exists()

    @pytest.mark.django_db
    def test_unsubscribe_private(self, client, auth_user):
        podcast = SubscriptionFactory(
            subscriber=auth_user, podcast=PodcastFactory(private=True)
        ).podcast

        response = client.delete(
            self.url(podcast),
            headers={
                "HX-Request": "true",
                "HX-Target": "subscribe-button",
            },
        )

        assert_404(response)

        assert Subscription.objects.filter(
            podcast=podcast, subscriber=auth_user
        ).exists()


class TestPrivateFeeds:
    url = reverse_lazy("podcasts:private_feeds")

    @pytest.mark.django_db
    def test_ok(self, client, auth_user):
        for podcast in PodcastFactory.create_batch(33, private=True):
            SubscriptionFactory(subscriber=auth_user, podcast=podcast)
        response = client.get(self.url)
        assert_200(response)
        assert response.context["page_obj"].paginator.count == 33

    @pytest.mark.django_db
    def test_empty(self, client, auth_user):
        PodcastFactory(private=True)
        response = client.get(self.url)
        assert_200(response)
        assert response.context["page_obj"].paginator.count == 0

    @pytest.mark.django_db
    def test_search(self, client, auth_user, faker):
        podcast = SubscriptionFactory(
            subscriber=auth_user,
            podcast=PodcastFactory(title=faker.unique.text(), private=True),
        ).podcast

        SubscriptionFactory(
            subscriber=auth_user,
            podcast=PodcastFactory(title="zzz", keywords="zzzz", private=True),
        )

        response = client.get(self.url, {"search": podcast.title})

        assert_200(response)

        assert len(response.context["page_obj"].object_list) == 1
        assert response.context["page_obj"].object_list[0] == podcast


class TestRemovePrivateFeed:
    @pytest.mark.django_db
    def test_ok(self, client, auth_user):
        podcast = PodcastFactory(private=True)
        SubscriptionFactory(podcast=podcast, subscriber=auth_user)

        response = client.delete(
            reverse("podcasts:remove_private_feed", args=[podcast.pk]),
            {"rss": podcast.rss},
        )
        assert response.url == reverse("podcasts:private_feeds")

        assert not Subscription.objects.filter(
            subscriber=auth_user, podcast=podcast
        ).exists()

    @pytest.mark.django_db
    def test_not_private_feed(self, client, auth_user):
        podcast = PodcastFactory(private=False)
        SubscriptionFactory(podcast=podcast, subscriber=auth_user)

        assert_404(
            client.delete(
                reverse("podcasts:remove_private_feed", args=[podcast.pk]),
                {"rss": podcast.rss},
            )
        )

        assert Subscription.objects.filter(
            subscriber=auth_user, podcast=podcast
        ).exists()


class TestAddPrivateFeed:
    url = reverse_lazy("podcasts:add_private_feed")

    @pytest.fixture
    def rss(self, faker):
        return faker.url()

    @pytest.mark.django_db
    def test_get(self, client, auth_user):
        assert_200(client.get(self.url))

    @pytest.mark.django_db
    def test_cancel(self, client, auth_user, rss):
        response = client.post(self.url, {"rss": rss, "action": "cancel"})
        assert response.url == reverse("podcasts:private_feeds")
        assert not Podcast.objects.exists()

    @pytest.mark.django_db
    def test_post_not_existing(self, client, auth_user, rss):
        response = client.post(self.url, {"rss": rss})
        assert response.url == reverse("podcasts:private_feeds")

        podcast = Subscription.objects.get(
            subscriber=auth_user, podcast__rss=rss
        ).podcast

        assert podcast.private

    @pytest.mark.django_db
    def test_existing_private(self, client, auth_user):
        podcast = PodcastFactory(private=True)

        response = client.post(self.url, {"rss": podcast.rss})
        assert response.url == podcast.get_absolute_url()

        assert Subscription.objects.filter(
            subscriber=auth_user, podcast=podcast
        ).exists()

    @pytest.mark.django_db
    def test_existing_public(self, client, auth_user):
        podcast = PodcastFactory(private=False)

        assert_200(client.post(self.url, {"rss": podcast.rss}))

        assert not Subscription.objects.filter(
            subscriber=auth_user, podcast=podcast
        ).exists()
