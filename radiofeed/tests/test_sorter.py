from __future__ import annotations

from radiofeed.sorter import Sorter


class TestSorter:
    def test_default_value(self, rf):
        req = rf.get("/")
        sorter = Sorter(req)
        assert sorter.value == "desc"
        assert sorter.is_desc

    def test_asc_value(self, rf):
        req = rf.get("/", {"order": "asc"})
        sorter = Sorter(req)
        assert sorter.value == "asc"
        assert sorter.is_asc

    def test_desc_value(self, rf):
        req = rf.get("/", {"order": "desc"})
        sorter = Sorter(req)
        assert sorter.value == "desc"
        assert sorter.is_desc

    def test_str(self, rf):
        req = rf.get("/")
        sorter = Sorter(req)
        assert str(sorter) == "desc"

    def test_qs_if_asc(self, rf):
        req = rf.get("/", {"order": "asc"})
        sorter = Sorter(req)
        assert sorter.qs == "order=desc"

    def test_qs_if_desc(self, rf):
        req = rf.get("/", {"order": "desc"})
        sorter = Sorter(req)
        assert sorter.qs == "order=asc"
