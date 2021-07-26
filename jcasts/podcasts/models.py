from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, TrigramSimilarity
from django.core.validators import MinLengthValidator
from django.db import models
from django.http import HttpRequest
from django.template.defaultfilters import striptags
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.text import slugify
from model_utils.models import TimeStampedModel

from jcasts.shared.db import FastCountMixin, SearchMixin
from jcasts.shared.template.defaulttags import unescape
from jcasts.shared.typedefs import AnyUser, AuthenticatedUser


class CategoryQuerySet(models.QuerySet):
    def search(self, search_term: str, base_similarity: float = 0.2) -> models.QuerySet:
        return self.annotate(
            similarity=TrigramSimilarity("name", force_str(search_term))
        ).filter(similarity__gte=base_similarity)


CategoryManager = models.Manager.from_queryset(CategoryQuerySet)


class Category(models.Model):

    name: str = models.CharField(max_length=100, unique=True)
    parent: Category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    # https://itunes.apple.com/search?term=podcast&genreId=1402&limit=20
    itunes_genre_id: int = models.IntegerField(
        verbose_name="iTunes Genre ID", null=True, blank=True, unique=True
    )

    objects = CategoryManager()

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    @property
    def slug(self) -> str:
        return slugify(self.name, allow_unicode=False)

    def get_absolute_url(self) -> str:
        return reverse("podcasts:category_detail", args=[self.pk, self.slug])


class PodcastQuerySet(FastCountMixin, SearchMixin, models.QuerySet):
    def for_feed_sync(self, now: datetime | None = None) -> models.QuerySet:
        now = now or timezone.now()
        weekday = now.isoweekday()

        recent = now - timedelta(days=7)
        first_tier = now - timedelta(days=30)
        second_tier = now - timedelta(days=60)
        third_tier = now - timedelta(days=90)

        weekdays = range(1, 8)

        daily_q = (
            # less than 30 days: check once a day
            models.Q(pub_date__range=(first_tier, recent))
            # last pub > 30 days: check every other day
            | models.Q(
                pub_date__range=(second_tier, first_tier),
                pub_date__iso_week_day__in=[
                    w for w in weekdays if w % 2 == weekday % 2
                ],
            )
            # last pub > 90 days: check every third day
            | models.Q(
                pub_date__range=(third_tier, second_tier),
                pub_date__iso_week_day__in=[
                    w for w in weekdays if w % 3 == weekday % 3
                ],
            )
            # last pub > 120 days: check once a week
            | models.Q(
                pub_date__lt=third_tier,
                pub_date__iso_week_day=weekday,
            )
        ) & models.Q(pub_date__hour=now.hour)

        return self.filter(
            models.Q(
                pub_date__isnull=True,
            )
            | models.Q(
                # recent: check twice a day
                pub_date__gte=recent,
                pub_date__hour__in=[now.hour, abs(now.hour - 12)],
            )
            | daily_q,
            active=True,
        ).distinct()


PodcastManager = models.Manager.from_queryset(PodcastQuerySet)


class Podcast(models.Model):

    rss: str = models.URLField(unique=True, max_length=500)
    active: bool = models.BooleanField(default=True)

    etag: str = models.TextField(blank=True)
    title: str = models.TextField()

    pub_date: datetime | None = models.DateTimeField(null=True, blank=True)

    num_episodes: int = models.PositiveIntegerField(default=0)

    cover_url: str | None = models.URLField(max_length=2083, null=True, blank=True)

    itunes: str = models.URLField(max_length=2083, null=True, blank=True, unique=True)

    language: str = models.CharField(
        max_length=2, default="en", validators=[MinLengthValidator(2)]
    )
    description: str = models.TextField(blank=True)
    link: str = models.URLField(max_length=2083, null=True, blank=True)
    keywords: str = models.TextField(blank=True)
    extracted_text: str = models.TextField(blank=True)
    owner: str = models.TextField(blank=True)

    created: datetime = models.DateTimeField(auto_now_add=True)
    updated: datetime = models.DateTimeField(auto_now=True)

    modified: datetime | None = models.DateTimeField(null=True, blank=True)

    explicit: bool = models.BooleanField(default=False)
    promoted: bool = models.BooleanField(default=False)

    categories: list[Category] = models.ManyToManyField(Category, blank=True)

    # received recommendation email
    recipients: list[AuthenticatedUser] = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="recommended_podcasts"
    )

    # HTTP error status
    error_status: int | None = models.PositiveSmallIntegerField(null=True, blank=True)

    # error fetching RSS
    exception: str = models.TextField(blank=True)

    # if permanent redirect to feed that already exists
    redirect_to: Podcast | None = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    search_vector: str = SearchVectorField(null=True, editable=False)

    objects = PodcastManager()

    class Meta:
        indexes = [
            models.Index(fields=["-created", "-pub_date"]),
            models.Index(fields=["-pub_date"]),
            models.Index(fields=["pub_date"]),
            GinIndex(fields=["search_vector"]),
        ]

    def __str__(self) -> str:
        return self.title or self.rss

    @cached_property
    def cleaned_title(self) -> str:
        return striptags(unescape(self.title))

    def get_absolute_url(self) -> str:
        return self.get_detail_url()

    def get_detail_url(self) -> str:
        return reverse("podcasts:podcast_detail", args=[self.pk, self.slug])

    def get_episodes_url(self) -> str:
        return reverse("podcasts:podcast_episodes", args=[self.pk, self.slug])

    def get_recommendations_url(self) -> str:
        return reverse("podcasts:podcast_recommendations", args=[self.pk, self.slug])

    def get_domain(self) -> str:
        return urlparse(self.rss).netloc.rsplit("www.", 1)[-1]

    @property
    def slug(self) -> str:
        return slugify(self.title, allow_unicode=False) or "podcast"

    def is_following(self, user: AnyUser) -> bool:
        if user.is_anonymous:
            return False
        return Follow.objects.filter(podcast=self, user=user).exists()

    def get_opengraph_data(self, request: HttpRequest) -> dict[str, str | int]:

        og_data: dict[str, str | int] = {
            "url": request.build_absolute_uri(self.get_absolute_url()),
            "title": f"{request.site.name} | {self.title}",
            "description": self.description,
            "keywords": ", ".join(self.keywords.split()),
        }

        if self.cover_url:
            og_data = {
                **og_data,
                "image": self.cover_url,
                "image_height": 200,
                "image_width": 200,
            }
        return og_data


class Follow(TimeStampedModel):

    user: AuthenticatedUser = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    podcast: Podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(name="uniq_follow", fields=["user", "podcast"])
        ]
        indexes = [models.Index(fields=["-created"])]


class RecommendationQuerySet(models.QuerySet):
    def bulk_delete(self) -> int:
        """More efficient quick delete"""
        return self._raw_delete(self.db)

    def for_user(self, user: AuthenticatedUser) -> models.QuerySet:
        podcast_ids = (
            set(
                user.favorite_set.select_related("episode__podcast").values_list(
                    "episode__podcast", flat=True
                )
            )
            | set(
                user.queueitem_set.select_related("episode__podcast").values_list(
                    "episode__podcast", flat=True
                )
            )
            | set(
                user.audiolog_set.select_related("episode__podcast").values_list(
                    "episode__podcast", flat=True
                )
            )
            | set(user.follow_set.values_list("podcast", flat=True))
        )

        return self.filter(podcast__pk__in=podcast_ids).exclude(
            recommended__pk__in=podcast_ids
            | set(user.recommended_podcasts.distinct().values_list("pk", flat=True))
        )


RecommendationManager = models.Manager.from_queryset(RecommendationQuerySet)


class Recommendation(models.Model):

    podcast: Podcast = models.ForeignKey(
        Podcast, related_name="+", on_delete=models.CASCADE
    )
    recommended: Podcast = models.ForeignKey(
        Podcast, related_name="+", on_delete=models.CASCADE
    )

    frequency: int = models.PositiveIntegerField(default=0)

    similarity: Decimal | None = models.DecimalField(
        decimal_places=10, max_digits=100, null=True, blank=True
    )

    objects = RecommendationManager()

    class Meta:
        indexes = [
            models.Index(fields=["podcast"]),
            models.Index(fields=["recommended"]),
            models.Index(fields=["-similarity", "-frequency"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["podcast", "recommended"], name="unique_recommendation"
            ),
        ]
