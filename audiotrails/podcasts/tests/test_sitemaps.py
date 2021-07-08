from audiotrails.podcasts.factories import CategoryFactory, PodcastFactory
from audiotrails.shared.assertions import assert_ok


class TestCategorySitemap:
    def test_get(self, client, db):
        CategoryFactory.create_batch(12)
        resp = client.get("/sitemap-categories.xml")
        assert_ok(resp)
        assert resp["Content-Type"] == "application/xml"


class TestPodcastSitemap:
    def test_get(self, client, db):
        PodcastFactory.create_batch(12)
        resp = client.get("/sitemap-podcasts.xml")
        assert_ok(resp)
        assert resp["Content-Type"] == "application/xml"
