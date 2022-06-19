from __future__ import annotations

import dataclasses

from datetime import datetime
from typing import Generator

import lxml.etree

from radiofeed.podcasts.parsers import converters, xml_parser

NAMESPACES: dict[str, str] = {
    "atom": "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "media": "http://search.yahoo.com/mrss/",
    "podcast": "https://podcastindex.org/namespace/1.0",
}


class RssParserError(ValueError):
    ...


@dataclasses.dataclass(frozen=True)
class Item:

    guid: str
    title: str
    pub_date: datetime

    media_url: str | None
    media_type: str

    link: str | None = None
    explicit: bool = False
    length: int | None = None
    season: int | None = None
    episode: int | None = None
    cover_url: str | None = None

    episode_type: str = ""
    duration: str = ""
    description: str = ""
    keywords: str = ""


@dataclasses.dataclass(frozen=True)
class Feed:

    title: str
    language: str

    link: str | None = None
    cover_url: str | None = None
    funding_text: str = ""
    funding_url: str | None = None
    owner: str = ""
    description: str = ""
    complete: bool = False
    explicit: bool = False

    categories: list[str] = dataclasses.field(default_factory=list)
    items: list[Item] = dataclasses.field(default_factory=list)

    @property
    def latest_pub_date(self) -> datetime | None:
        try:
            return max([item.pub_date for item in self.items])
        except ValueError:
            return None


def parse_rss(content: bytes) -> Feed:

    try:

        feed = parse_feed(next(xml_parser.iterparse(content, "channel")))

        if not feed.items:
            raise ValueError("no items in RSS feed")

        return feed

    except (StopIteration, ValueError, lxml.etree.XMLSyntaxError) as e:
        raise RssParserError from e


def parse_feed(channel: lxml.etree.Element) -> Feed:
    with xml_parser.xpath_finder(channel, NAMESPACES) as finder:
        return Feed(
            title=finder.first("title/text()", required=True),
            link=converters.url(finder.first("link/text()")),
            language=converters.language(finder.first("language/text()")),
            explicit=converters.explicit(finder.first("itunes:explicit/text()")),
            cover_url=converters.url(
                finder.first("itunes:image/@href", "image/url/text()")
            ),
            funding_url=converters.url(finder.first("podcast:funding/@url")),
            funding_text=finder.first("podcast:funding/text()"),
            description=finder.first(
                "description/text()",
                "itunes:summary/text()",
            ),
            owner=finder.first(
                "itunes:author/text()",
                "itunes:owner/itunes:name/text()",
            ),
            complete=converters.boolean(finder.first("itunes:complete/text()")),
            categories=finder.all("//itunes:category/@text"),
            items=list(parse_items(channel)),
        )


def parse_items(channel: lxml.etree.Element) -> Generator[Item, None, None]:
    for item in channel.iterfind("item"):
        try:
            yield parse_item(item)
        except ValueError:
            continue


def parse_item(item: lxml.etree.Element) -> Item:
    with xml_parser.xpath_finder(item, NAMESPACES) as finder:
        return Item(
            guid=finder.first("guid/text()", required=True),
            title=finder.first("title/text()", required=True),
            pub_date=converters.pub_date(finder.first("pubDate/text()", required=True)),
            link=converters.url(finder.first("link/text()")),
            media_url=converters.url(
                finder.first(
                    "enclosure//@url",
                    "media:content//@url",
                    required=True,
                ),
                raises=True,
            ),
            media_type=converters.audio(
                finder.first(
                    "enclosure//@type",
                    "media:content//@type",
                    required=True,
                )
            ),
            length=converters.integer(
                finder.first(
                    "enclosure//@length",
                    "media:content//@fileSize",
                )
            ),
            explicit=converters.explicit(finder.first("itunes:explicit/text()")),
            cover_url=converters.url(finder.first("itunes:image/@href")),
            episode=converters.integer(finder.first("itunes:episode/text()")),
            season=converters.integer(finder.first("itunes:season/text()")),
            description=finder.first(
                "content:encoded/text()",
                "description/text()",
                "itunes:summary/text()",
            ),
            duration=converters.duration(finder.first("itunes:duration/text()")),
            episode_type=finder.first("itunes:episodetype/text()", default="full"),
            keywords=" ".join(finder.all("category/text()")),
        )
