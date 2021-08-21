from __future__ import annotations

import re

from functools import lru_cache

from django.template.defaultfilters import striptags
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

from jcasts.shared import cleaners

"""Additional language-specific stopwords"""

ENGLISH_DAYS: list[str] = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "mon",
    "tue",
    "wed",
    "thu",
    "fri",
    "sat",
    "sun",
]

ENGLISH_NUMBERS: list[str] = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
]

ENGLISH_MONTHS: list[str] = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
]

ENGLISH_MISC_WORDS: list[str] = [
    "across",
    "advice",
    "along",
    "also",
    "always",
    "answer",
    "around",
    "audio",
    "available",
    "back",
    "become",
    "behind",
    "best",
    "better",
    "beyond",
    "big",
    "biggest",
    "bring",
    "brings",
    "change",
    "channel",
    "city",
    "come",
    "content",
    "conversation",
    "course",
    "daily",
    "date",
    "day",
    "days",
    "different",
    "discussion",
    "dont",
    "dr",
    "end",
    "enjoy",
    "episode",
    "episodes",
    "even",
    "ever",
    "every",
    "everyone",
    "everything",
    "favorite",
    "feature",
    "featuring",
    "feed",
    "field",
    "find",
    "first",
    "focus",
    "follow",
    "full",
    "fun",
    "get",
    "give",
    "go",
    "going",
    "good",
    "gmt",
    "great",
    "guest",
    "happen",
    "happening",
    "hear",
    "host",
    "hosted",
    "hour",
    "idea",
    "impact",
    "important",
    "including",
    "information",
    "inside",
    "insight",
    "interesting",
    "interview",
    "issue",
    "join",
    "journalist",
    "keep",
    "know",
    "knowledge",
    "known",
    "latest",
    "leading",
    "learn",
    "let",
    "life",
    "like",
    "listen",
    "listener",
    "little",
    "live",
    "look",
    "looking",
    "made",
    "make",
    "making",
    "many",
    "matter",
    "medium",
    "member",
    "minute",
    "moment",
    "month",
    "mr",
    "mrs",
    "ms",
    "much",
    "name",
    "need",
    "never",
    "new",
    "news",
    "next",
    "night",
    "offer",
    "open",
    "original",
    "other",
    "others",
    "part",
    "past",
    "people",
    "personal",
    "perspective",
    "place",
    "podcast",
    "podcasts",
    "premium",
    "present",
    "problem",
    "produced",
    "producer",
    "product",
    "production",
    "question",
    "radio",
    "read",
    "real",
    "really",
    "review",
    "right",
    "scene",
    "season",
    "see",
    "series",
    "set",
    "share",
    "short",
    "show",
    "shows",
    "side",
    "sign",
    "sir",
    "small",
    "something",
    "sometimes",
    "sound",
    "special",
    "sponsor",
    "start",
    "stories",
    "story",
    "subscribe",
    "support",
    "take",
    "tale",
    "talk",
    "talking",
    "team",
    "tell",
    "thing",
    "think",
    "thought",
    "time",
    "tip",
    "today",
    "together",
    "top",
    "topic",
    "training",
    "true",
    "truth",
    "understand",
    "unique",
    "use",
    "ustream",
    "video",
    "visit",
    "voice",
    "want",
    "way",
    "week",
    "weekly",
    "welcome",
    "well",
    "were",
    "what",
    "word",
    "work",
    "world",
    "would",
    "year",
    "years",
    "youll",
    "youre",
]

CORPORATES: list[str] = [
    "apple",
    "patreon",
    "spotify",
    "stitcher",
    "itunes",
]

STOPWORDS: dict[str, list[str]] = {
    "en": ENGLISH_DAYS
    + ENGLISH_MONTHS
    + ENGLISH_NUMBERS
    + ENGLISH_MISC_WORDS
    + CORPORATES
}
NLTK_LANGUAGES: dict[str, str] = {
    "ar": "arabic",
    "az": "azerbaijani",
    "da": "danish",
    "de": "german",
    "el": "greek",
    "en": "english",
    "es": "spanish",
    "fi": "finnish",
    "fr": "french",
    "hu": "hungarian",
    "id": "indonesian",
    "it": "italian",
    "kk": "kazakh",
    "ne": "nepali",
    "nl": "dutch",
    "no": "norwegian",
    "pt": "portuguese",
    "ro": "romanian",
    "ru": "russian",
    "sl": "slovene",
    "sv": "swedish",
    "tg": "tajik",
    "tr": "turkish",
}

tokenizer = RegexpTokenizer(r"\w+")
lemmatizer = WordNetLemmatizer()


@lru_cache()
def get_stopwords(language: str) -> list[str]:
    try:
        return stopwords.words(NLTK_LANGUAGES[language]) + STOPWORDS.get(language, [])
    except KeyError:
        return []


def clean_text(text: str) -> str:
    """Remove HTML tags and entities, punctuation and numbers."""
    text = cleaners.unescape(striptags(text.strip()))
    text = re.sub(r"([^\s\w]|_:.?-)+", "", text)
    text = re.sub(r"[0-9]+", "", text)
    return text


def extract_keywords(language: str, text: str) -> list[str]:

    if not (text := clean_text(text).lower()):
        return []

    stopwords = get_stopwords(language)

    return [token for token in tokenize(text) if token and token not in stopwords]


def tokenize(text: str) -> list[str]:
    return [lemmatizer.lemmatize(token) for token in tokenizer.tokenize(text)]
