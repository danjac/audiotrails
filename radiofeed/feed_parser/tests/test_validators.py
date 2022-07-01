import pytest

from radiofeed.feed_parser import validators


class TestRequired:
    @pytest.mark.parametrize(
        "value,raises",
        [
            ("ok", False),
            ("", True),
            (None, True),
        ],
    )
    def test_required(self, value, raises):

        if raises:
            with pytest.raises(ValueError):
                validators.required(None, None, value)
        else:
            validators.required(None, None, value)


class TestUrl:
    @pytest.mark.parametrize(
        "value,raises",
        [
            ("http://example.com", False),
            ("https://example.com", False),
            ("example", True),
        ],
    )
    def test_url(self, value, raises):
        if raises:
            with pytest.raises(ValueError):
                validators.url(None, None, value)
        else:
            validators.url(None, None, value)
