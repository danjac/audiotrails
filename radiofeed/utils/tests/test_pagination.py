from __future__ import annotations

from radiofeed.utils.pagination import pagination_url


class TestPaginationUrl:
    def test_append_page_number_to_querystring(self, rf):

        req = rf.get("/search/", {"query": "test"})
        url = pagination_url(req, 5)
        assert url.startswith("/search/?")
        assert "query=test" in url
        assert "page=5" in url
