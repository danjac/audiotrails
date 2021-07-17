import pytest

from django.contrib.admin.sites import AdminSite

from jcasts.episodes.admin import EpisodeAdmin
from jcasts.episodes.factories import EpisodeFactory
from jcasts.episodes.models import Episode


class TestEpisodeAdmin:
    @pytest.fixture
    def admin(self):
        return EpisodeAdmin(Episode, AdminSite())

    def test_episode_title(self, db, admin):
        episode = EpisodeFactory(title="testing")
        assert admin.episode_title(episode) == "testing"

    def test_podcast_title(self, db, admin):
        episode = EpisodeFactory(podcast__title="testing")
        assert admin.podcast_title(episode) == "testing"

    def test_get_search_results_no_search_term(self, rf, db, admin):
        EpisodeFactory.create_batch(3)
        qs, _ = admin.get_search_results(rf.get("/"), Episode.objects.all(), "")
        assert qs.count() == 3

    def test_get_search_results(self, rf, db, admin):
        EpisodeFactory.create_batch(3)

        episode = EpisodeFactory(title="testing python")

        qs, _ = admin.get_search_results(
            rf.get("/"), Episode.objects.all(), "testing python"
        )
        assert qs.count() == 1
        assert qs.first() == episode
