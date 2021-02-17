import datetime

from django.utils import timezone

import pytest

from ..factories import (
    AudioLogFactory,
    EpisodeFactory,
    FavoriteFactory,
    QueueItemFactory,
)
from ..models import AudioLog, Episode, Favorite

pytestmark = pytest.mark.django_db


class TestEpisodeManager:
    def test_with_current_time_if_anonymous(self, anonymous_user):
        EpisodeFactory()
        episode = Episode.objects.with_current_time(anonymous_user).first()
        assert episode.current_time == 0
        assert episode.completed is False
        assert episode.listened is None

    def test_with_current_time_if_not_played(self, user):
        EpisodeFactory()
        episode = Episode.objects.with_current_time(user).first()
        assert episode.current_time is None
        assert episode.completed is None
        assert episode.listened is None

    def test_with_current_time_if_played(self, user):
        log = AudioLogFactory(user=user, current_time=20, updated=timezone.now())
        episode = Episode.objects.with_current_time(user).first()
        assert episode.current_time == 20
        assert episode.completed is None
        assert episode.listened == log.updated

    def test_with_current_time_if_completed(self, user):
        log = AudioLogFactory(
            user=user, current_time=20, completed=timezone.now(), updated=timezone.now()
        )
        episode = Episode.objects.with_current_time(user).first()
        assert episode.current_time == 20
        assert episode.completed is not None
        assert episode.listened == log.updated

    def test_search(self):
        EpisodeFactory(title="testing")
        assert Episode.objects.search("testing").count() == 1


class TestEpisodeModel:
    def test_get_media_metadata(self, episode):
        data = episode.get_media_metadata()
        assert data["title"] == episode.title
        assert data["album"] == episode.podcast.title
        assert data["artist"] == episode.podcast.authors

    def test_slug(self):
        episode = Episode(title="Testing")
        assert episode.slug == "testing"

    def test_slug_if_title_empty(self):
        assert Episode().slug == "episode"

    def test_log_activity_new(self, user, episode):
        log, created = episode.log_activity(user, current_time=1000)
        assert created
        assert log.current_time == 1000

    def test_log_activity_existing(self, user, episode):
        last_logged_at = timezone.now() - datetime.timedelta(days=2)
        AudioLogFactory(
            user=user, episode=episode, current_time=1000, updated=last_logged_at
        )
        log, created = episode.log_activity(user, current_time=1030)
        assert not created
        assert log.current_time == 1030
        assert log.updated > last_logged_at

    def test_get_duration_in_seconds_if_empty(self):
        assert Episode().get_duration_in_seconds() == 0
        assert Episode(duration="").get_duration_in_seconds() == 0

    def test_duration_in_seconds_if_non_numeric(self):
        assert Episode(duration="NaN").get_duration_in_seconds() == 0

    def test_duration_in_seconds_if_seconds_only(self):
        assert Episode(duration="60").get_duration_in_seconds() == 60

    def test_duration_in_seconds_if_minutes_and_seconds(self):
        assert Episode(duration="2:30").get_duration_in_seconds() == 150

    def test_duration_in_seconds_if_hours_minutes_and_seconds(self):
        assert Episode(duration="2:30:30").get_duration_in_seconds() == 9030

    def test_has_next_previous_episode(self, episode):
        assert episode.get_next_episode() is None
        assert episode.get_previous_episode() is None

        next_episode = EpisodeFactory(
            podcast=episode.podcast,
            pub_date=episode.pub_date + datetime.timedelta(days=2),
        )

        previous_episode = EpisodeFactory(
            podcast=episode.podcast,
            pub_date=episode.pub_date - datetime.timedelta(days=2),
        )

        EpisodeFactory(
            podcast=episode.podcast,
            pub_date=episode.pub_date - datetime.timedelta(days=3),
        )

        assert episode.get_next_episode() == next_episode
        assert episode.get_previous_episode() == previous_episode

    def is_favorited_anonymous(self, episode, anonymous_user):
        assert not episode.is_favorited(anonymous_user)

    def is_favorited_false(self, episode, user):
        assert not episode.is_favorited(user)

    def is_favorited_true(self):
        fave = FavoriteFactory()
        assert fave.episode.is_favorited(fave.user)

    def is_queued_anonymous(self, episode, anonymous_user):
        assert not episode.is_queued(anonymous_user)

    def is_queued_false(self, episode, user):
        assert not episode.is_queued(user)

    def is_queued_true(self):
        item = QueueItemFactory()
        assert item.episode.is_queued(item.user)

    def test_get_opengraph_data(self, rf, episode, site):
        req = rf.get("/")
        req.site = site
        data = episode.get_opengraph_data(req)
        assert episode.title in data["title"]
        assert data["url"] == "http://testserver" + episode.get_absolute_url()


class TestFavoriteManager:
    def test_search(self):
        episode = EpisodeFactory(title="testing")
        FavoriteFactory(episode=episode)
        assert Favorite.objects.search("testing").count() == 1


class TestAudioLogManager:
    def test_search(self):
        episode = EpisodeFactory(title="testing")
        AudioLogFactory(episode=episode)
        assert AudioLog.objects.search("testing").count() == 1
