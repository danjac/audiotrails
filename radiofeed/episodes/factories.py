# Standard Library
import uuid

# Django
from django.utils import timezone

# Third Party Libraries
from factory import Faker, LazyFunction, SubFactory
from factory.django import DjangoModelFactory

# RadioFeed
from radiofeed.podcasts.factories import PodcastFactory
from radiofeed.users.factories import UserFactory

# Local
from .models import Bookmark, Episode, History


class EpisodeFactory(DjangoModelFactory):

    guid = LazyFunction(lambda: uuid.uuid4().hex)
    podcast = SubFactory(PodcastFactory)
    title = Faker("text")
    description = Faker("text")
    media_url = Faker("url")
    media_type = "audio/mpeg"
    pub_date = LazyFunction(timezone.now)

    class Meta:
        model = Episode


class BookmarkFactory(DjangoModelFactory):
    episode = SubFactory(EpisodeFactory)
    user = SubFactory(UserFactory)

    class Meta:
        model = Bookmark


class HistoryFactory(DjangoModelFactory):
    episode = SubFactory(EpisodeFactory)
    user = SubFactory(UserFactory)
    updated = LazyFunction(timezone.now)
    current_time = 1000

    class Meta:
        model = History
