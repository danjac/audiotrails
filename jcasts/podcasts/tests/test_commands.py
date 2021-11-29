from django.core.management import call_command

from jcasts.podcasts.factories import CategoryFactory, PodcastFactory
from jcasts.podcasts.models import Category, Podcast, Recommendation
from jcasts.users.factories import UserFactory


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
