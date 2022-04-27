from django.conf import settings
from django.urls import reverse, reverse_lazy

from jcasts.common.asserts import assert_ok
from jcasts.episodes.factories import AudioLogFactory, BookmarkFactory, EpisodeFactory
from jcasts.podcasts.factories import SubscriptionFactory
from jcasts.users.models import User


class TestUserPreferences:
    url = reverse_lazy("users:preferences")

    def test_get(self, client, auth_user, django_assert_num_queries):
        with django_assert_num_queries(3):
            response = client.get(self.url)
        assert_ok(response)

    def test_post(self, client, auth_user, django_assert_num_queries):
        with django_assert_num_queries(4):
            response = client.post(
                self.url,
                {
                    "send_email_notifications": False,
                    "autoplay": True,
                },
            )

        assert_ok(response)

        auth_user.refresh_from_db()

        assert not auth_user.send_email_notifications


class TestUserStats:
    def test_stats(self, client, auth_user, podcast, django_assert_num_queries):

        SubscriptionFactory(podcast=podcast, user=auth_user)
        AudioLogFactory(episode=EpisodeFactory(podcast=podcast), user=auth_user)
        AudioLogFactory(episode=EpisodeFactory(podcast=podcast), user=auth_user)
        AudioLogFactory(user=auth_user)
        BookmarkFactory(user=auth_user)

        with django_assert_num_queries(8):
            response = client.get(reverse("users:stats"))
        assert_ok(response)
        assert response.context["stats"]["subscribed"] == 1
        assert response.context["stats"]["listened"] == 3


class TestExportPodcastFeeds:
    def test_page(self, client, auth_user, django_assert_num_queries):
        with django_assert_num_queries(3):
            assert_ok(client.get(reverse("users:export_podcast_feeds")))

    def test_export_opml(self, client, subscription, django_assert_num_queries):
        with django_assert_num_queries(4):
            response = client.get(reverse("users:export_podcast_feeds_opml"))
        assert_ok(response)
        assert response["Content-Type"] == "application/xml"

    def test_export_csv(self, client, subscription, django_assert_num_queries):
        with django_assert_num_queries(4):
            response = client.get(reverse("users:export_podcast_feeds_csv"))
        assert_ok(response)
        assert response["Content-Type"] == "text/csv"

    def test_export_json(self, client, subscription, django_assert_num_queries):
        with django_assert_num_queries(4):
            response = client.get(reverse("users:export_podcast_feeds_json"))
        assert_ok(response)
        assert response["Content-Type"] == "application/json"


class TestDeleteAccount:
    url = reverse_lazy("users:delete_account")

    def test_get(self, client, auth_user, django_assert_num_queries):
        # make sure we don't accidentally delete account on get request
        with django_assert_num_queries(3):
            response = client.get(self.url)
        assert_ok(response)
        assert User.objects.exists()

    def test_post_unconfirmed(self, client, auth_user, django_assert_num_queries):
        with django_assert_num_queries(3):
            response = client.post(self.url)
        assert_ok(response)
        assert User.objects.exists()

    def test_post_confirmed(self, client, auth_user, django_assert_num_queries):
        with django_assert_num_queries(15):
            response = client.post(self.url, {"confirm-delete": True})
        assert response.url == settings.HOME_URL
        assert not User.objects.exists()
