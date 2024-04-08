import functools
from collections.abc import Iterator

from radiofeed.feedparser.xpath_parser import XPathParser


def parse_opml(content: bytes) -> Iterator[str]:
    """Parse OPML document and return podcast URLs"""

    return _opml_parser().parse(content)


class _OPMLParser:
    """Parse OPML document."""

    def __init__(self) -> None:
        self._parser = XPathParser()

    def parse(self, content: bytes) -> Iterator[str]:
        """Parse OPML content."""
        yield from self._parser.itervalues(
            self._parser.find(content, "opml", "body"),
            ".//outline/@xmlUrl",
        )


@functools.cache
def _opml_parser() -> _OPMLParser:
    return _OPMLParser()
