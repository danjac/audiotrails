import http

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from turbo_response.constants import TURBO_STREAM_MIME_TYPE

from audiotrails.episodes.factories import (
    AudioLogFactory,
    EpisodeFactory,
    FavoriteFactory,
)
from audiotrails.podcasts.factories import FollowFactory, PodcastFactory

from ..factories import UserFactory

User = get_user_model()


class UserPreferencesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get(self):
        resp = self.client.get(reverse("user_preferences"))
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)

    def test_post(self):
        url = reverse("user_preferences")
        resp = self.client.post(url, {"send_recommendations_email": False})
        self.assertRedirects(resp, url, status_code=http.HTTPStatus.SEE_OTHER)
        self.user.refresh_from_db()
        assert not self.user.send_recommendations_email


class UserStatsTests(TestCase):
    def test_stats(self):
        podcast = PodcastFactory()
        user = UserFactory()
        self.client.force_login(user)

        FollowFactory(podcast=podcast, user=user)
        AudioLogFactory(episode=EpisodeFactory(podcast=podcast), user=user)
        AudioLogFactory(episode=EpisodeFactory(podcast=podcast), user=user)
        AudioLogFactory(user=user)
        FavoriteFactory(user=user)
        resp = self.client.get(reverse("user_stats"))
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertEqual(resp.context["stats"]["follows"], 1)
        self.assertEqual(resp.context["stats"]["listened"], 3)


class ExportPodcastFeedsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.podcast = PodcastFactory()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get(self):
        resp = self.client.get(reverse("export_podcast_feeds"))
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)

    def test_export_opml(self):
        FollowFactory(podcast=self.podcast, user=self.user)
        resp = self.client.post(reverse("export_podcast_feeds"), {"format": "opml"})
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertEqual(resp["Content-Type"], "application/xml")

    def test_export_csv(self):
        FollowFactory(podcast=self.podcast, user=self.user)
        resp = self.client.post(reverse("export_podcast_feeds"), {"format": "csv"})
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertEqual(resp["Content-Type"], "text/csv")


class TestDeleteAccount:
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get(self):
        # make sure we don't accidentally delete account on get request
        resp = self.client.get(reverse("delete_account"))
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertTrue(User.objects.exists())

    def test_post_unconfirmed(self, client):
        resp = self.client.post(reverse("delete_account"))
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertTrue(User.objects.exists())

    def test_post_confirmed(self):
        resp = self.client.post(reverse("delete_account"), {"confirm-delete": True})
        self.assertRedirects(resp, settings.HOME_URL)
        self.assertFalse(User.objects.exists())


class TestAcceptCookies:
    def test_post(self):
        resp = self.client.post(reverse("accept_cookies"))
        self.assertRedirects(resp, settings.HOME_URL)
        self.assertFalse("accept-cookies" in resp.cookies)

    def test_post_turbo(self, client):
        resp = client.post(
            reverse("accept_cookies"), HTTP_ACCEPT=TURBO_STREAM_MIME_TYPE
        )
        self.assertEqual(resp.status_code, http.HTTPStatus.OK)
        self.assertFalse("accept-cookies" in resp.cookies)
