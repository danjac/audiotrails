from __future__ import annotations

import datetime
import pathlib

from zoneinfo import ZoneInfo

import pytest

from radiofeed.common.utils import html
from radiofeed.common.utils.crypto import make_content_hash
from radiofeed.common.utils.dates import parse_date
from radiofeed.common.utils.iterators import batcher
from radiofeed.common.utils.text import clean_text, get_stopwords, tokenize
from radiofeed.common.utils.xml import XPathFinder, parse_xml, xpath_finder


class TestMakeContentHash:
    def test_hash_identical(self):
        assert make_content_hash(b"ok") == make_content_hash(b"ok")


class TestXPathFinder:
    def read_mock_file(self, mock_filename="rss_mock.xml"):
        return (pathlib.Path(__file__).parent / "mocks" / mock_filename).read_bytes()

    @pytest.fixture
    def channel(self):
        return next(parse_xml(self.read_mock_file(), "channel"))

    def test_contexttmanager(self, channel):
        with xpath_finder(channel) as finder:
            assert finder.first("title/text()") == "Mysterious Universe"

    def test_iter(self, channel):
        assert list(XPathFinder(channel).iter("title/text()")) == [
            "Mysterious Universe"
        ]

    def test_to_dict(self, channel):

        assert XPathFinder(channel).to_dict(
            title="title/text()",
            cover_url=(
                "itunes:image/@href",
                "image/url/text()",
            ),
            editor="managingEditor2/text()",
        ) == {
            "title": "Mysterious Universe",
            "cover_url": "https://mysteriousuniverse.org/wp-content/uploads/2018/11/itunes_14k.jpg",
            "editor": None,
        }

    def test_first_exists(self, channel):
        assert XPathFinder(channel).first("title/text()") == "Mysterious Universe"

    def test_find_first_matching(self, channel):
        assert (
            XPathFinder(channel).first("editor/text()", "managingEditor/text()")
            == "sales@mysteriousuniverse.org (8th Kind)"
        )

    def test_default(self, channel):
        assert (
            XPathFinder(channel).first("editor/text()", "managingEditor2/text()")
            is None
        )


class TestStopwords:
    def test_get_stopwords_if_any(self):
        assert get_stopwords("en")

    def test_get_stopwords_if_none(self):
        assert get_stopwords("ka") == set()


class TestTokenize:
    def test_extract_if_empty(self):
        assert tokenize("en", "   ") == []

    def test_extract(self):
        assert tokenize("en", "the cat sits on the mat") == [
            "cat",
            "sits",
            "mat",
        ]

    def test_extract_attribute_error(self, mocker):
        mocker.patch(
            "radiofeed.common.utils.text._lemmatizer.lemmatize",
            side_effect=AttributeError,
        )
        assert tokenize("en", "the cat sits on the mat") == []


class TestCleanText:
    def test_remove_html_tags(self):
        assert clean_text("<p>test</p>") == "test"

    def test_remove_numbers(self):
        assert clean_text("Tuesday, September 1st, 2020") == "Tuesday September st "


UTC = ZoneInfo(key="UTC")


class TestClean:
    def test_if_safe(self):
        text = "<p>testing with paras</p>"
        assert html.clean(text) == text

    def test_has_link_link(self):
        text = '<a href="http://reddit.com">Reddit</a>'
        clean = html.clean(text)
        assert 'target="_blank"' in clean
        assert 'rel="noopener noreferrer nofollow"' in clean

    def test_unsafe(self):
        text = "<script>alert('xss ahoy!')</script>"
        assert html.clean(text) == "alert('xss ahoy!')"


class TestStripHtml:
    @pytest.mark.parametrize(
        "value,expected",
        [
            (None, ""),
            ("", ""),
            ("", ""),
            ("<p>this &amp; that</p>", "this & that"),
        ],
    )
    def test_strip_html(self, value, expected):
        return html.strip_html(value) == expected


class TestMarkup:
    @pytest.mark.parametrize(
        "value,expected",
        [
            (None, ""),
            (" ", ""),
            ("*test*", "<b>test</b>"),
            ("<p>test</p>", "<p>test</p>"),
            ("<script>alert('xss ahoy!')</script>", "alert('xss ahoy!')"),
        ],
    )
    def test_markup(self, value, expected):
        return html.markup(value) == expected


class TestParseDate:
    def test_empty_str(self):
        assert parse_date("") is None

    def test_none(self):
        assert parse_date(None) is None

    def test_invalid_offset(self):
        assert parse_date("Sun, 14 Jan 2018 21:38:44 -4400") == datetime.datetime(
            2018, 1, 14, 21, 38, 44, tzinfo=UTC
        )

    def test_not_tz_aware(self):
        dt = datetime.datetime(2020, 6, 19, 16, 58, 3)
        new_dt = parse_date(dt)

        assert new_dt.tzinfo == UTC

    def test_datetime(self):
        dt = datetime.datetime(2020, 6, 19, 16, 58, 3, tzinfo=UTC)
        assert parse_date(dt) == dt

    def test_date(self):
        dt = datetime.date(2020, 6, 19)
        assert parse_date(dt) == datetime.datetime(2020, 6, 19, 0, 0, 0, tzinfo=UTC)

    def test_valid_str(self):
        dt = datetime.datetime(2020, 6, 19, 16, 58, 3, tzinfo=UTC)
        assert parse_date("Fri, 19 Jun 2020 16:58:03 +0000") == dt

    def test_no_tz_in_str(self):
        dt = datetime.datetime(2020, 6, 19, 16, 58, 3, tzinfo=UTC)
        assert parse_date("Fri, 19 Jun 2020 16:58:03") == dt

    def test_invalid_str(self):
        assert parse_date("Fri, 33 June 2020 16:58:03 +0000") is None


class TestBatcher:
    def test_batcher(self):
        batches = list(batcher(range(0, 100), batch_size=10))
        assert len(batches) == 10
        assert batches[0] == list(range(0, 10))
