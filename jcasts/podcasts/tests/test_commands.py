import pytest

from django.core.management import call_command
from django.core.management.base import CommandError

from jcasts.podcasts.factories import CategoryFactory, PodcastFactory
from jcasts.podcasts.models import Category, Podcast, Recommendation
from jcasts.users.factories import UserFactory


class TestPodping:
    def test_command(self, mocker, faker):

        urls = [faker.url() for _ in range(3)]

        mock_updates = mocker.patch(
            "jcasts.podcasts.podping.get_updates", return_value=iter(urls)
        )
        mocker.patch("itertools.count", return_value=[3])

        call_command("podping")
        mock_updates.assert_called_with(15)

    def test_raise_exception(self, mocker, faker):

        mocker.patch("jcasts.podcasts.podping.get_updates", side_effect=ValueError)
        mocker.patch("itertools.count", return_value=[3])

        with pytest.raises(CommandError):
            call_command("podping")

    def test_keep_alive(self, mocker, faker):
        urls = [faker.url() for _ in range(30)]

        def get_updates(minutes):
            url = urls.pop()
            if len(urls) % 2 == 1:
                raise ValueError
            yield url

        mocker.patch("jcasts.podcasts.podping.get_updates", get_updates)
        mocker.patch("itertools.count", return_value=urls)

        call_command("podping", keep_alive=True)


class TestSubscribePodcasts:
    hub = "https://amazinglybrilliant.superfeedr.com/"
    url = "https://podnews.net/rss"

    @pytest.fixture
    def mock_subscribe(self, mocker):
        return mocker.patch("jcasts.podcasts.websub.subscribe.delay")

    def test_command(self, db, mock_subscribe):
        podcast = PodcastFactory(websub_url=self.url, websub_hub=self.hub)

        call_command("subscribe_podcasts")
        mock_subscribe.assert_called_with(podcast.id)

    def test_clear_exceptions(self, db, mock_subscribe):
        podcast = PodcastFactory(
            websub_url=self.url,
            websub_hub=self.hub,
            websub_exception="oops",
            websub_status=Podcast.WebSubStatus.ERROR,
        )

        call_command("subscribe_podcasts", clear=True)
        mock_subscribe.assert_called_with(podcast.id)

        podcast.refresh_from_db()
        assert podcast.websub_exception == ""
        assert podcast.websub_status is None


class TestSeedPodcastData:
    def test_command(self, db):

        call_command("seed_podcast_data")

        assert Category.objects.count() == 110
        assert Podcast.objects.count() == 294


class TestSendRecommendationEmails:
    def test_command(self, db, mocker):

        yes = UserFactory(send_recommendations_email=True)
        UserFactory(send_recommendations_email=False)
        UserFactory(send_recommendations_email=True, is_active=False)

        mock_send = mocker.patch(
            "jcasts.podcasts.emails.send_recommendations_email.delay"
        )

        call_command("send_recommendation_emails")

        assert len(mock_send.mock_calls) == 1
        assert mock_send.call_args == ((yes,),)


class TestMakeRecommendations:
    def test_command(self, db):
        category = CategoryFactory(name="Science")

        PodcastFactory(
            extracted_text="Cool science podcast science physics astronomy",
            categories=[category],
        )
        PodcastFactory(
            extracted_text="Another cool science podcast science physics astronomy",
            categories=[category],
        )

        call_command("make_recommendations")

        assert Recommendation.objects.count() == 2


class TestParsePodcastFeeds:
    def test_command(self, db, mock_parse_podcast_feed):
        podcast = PodcastFactory(pub_date=None)
        call_command("parse_podcast_feeds")
        mock_parse_podcast_feed.assert_called_with(podcast.id)
