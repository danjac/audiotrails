from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.text import slugify

from radiofeed.fast_count import FastCountQuerySetMixin
from radiofeed.html import strip_html
from radiofeed.search import SearchQuerySetMixin

if TYPE_CHECKING:  # pragma: no cover
    from radiofeed.users.models import User


class CategoryQuerySet(models.QuerySet):
    """Custom QuerySet for Category model."""

    def search(self, search_term) -> models.QuerySet[Category]:
        """Does a simple search for categories."""
        if value := force_str(search_term):
            return self.filter(name__icontains=value)
        return self.none()


class Category(models.Model):
    """iTunes category."""

    name = models.CharField(max_length=100, unique=True)
    parent: Category | None = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    objects: models.Manager[Category] = CategoryQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("name",)

    def __str__(self) -> str:
        """Returns category name."""
        return self.name

    def get_absolute_url(self) -> str:
        """Absolute URL to a category."""
        return reverse(
            "podcasts:category_detail",
            kwargs={
                "category_id": self.pk,
                "slug": self.slug,
            },
        )

    @cached_property
    def slug(self) -> str:
        """Returns slugified name."""
        return slugify(self.name, allow_unicode=False)


class PodcastQuerySet(
    FastCountQuerySetMixin,
    SearchQuerySetMixin,
    models.QuerySet,
):
    """Custom QuerySet of Podcast model."""

    def search(self, search_term) -> models.QuerySet[Podcast]:
        """Does standard full text search, prioritizing exact search results.

        Annotates `exact_match` to indicate such results.
        """
        if not search_term:
            return self.none()

        qs = super().search(search_term)

        exact_matches_qs = (
            self.alias(title_lower=models.functions.Lower("title"))
            .filter(title_lower=force_str(search_term).casefold())
            .values_list("pk", flat=True)
        )
        qs = qs | self.filter(pk__in=exact_matches_qs)

        return qs.annotate(
            exact_match=models.Case(
                models.When(pk__in=exact_matches_qs, then=models.Value(1)),
                default=models.Value(0),
            )
        )

    def subscribed(self, user: User) -> models.QuerySet[Podcast]:
        """Returns podcasts subscribed by user."""
        return self.alias(
            is_subscribed=models.Exists(
                user.subscriptions.filter(
                    podcast=models.OuterRef("pk"),
                )
            )
        ).filter(is_subscribed=True)


class Podcast(models.Model):
    """Podcast channel or feed."""

    class ParserError(models.TextChoices):
        DUPLICATE = "duplicate", "Duplicate"
        INACCESSIBLE = "inaccessible", "Inaccessible"
        INVALID_DATA = "invalid_data", "Invalid Data"
        INVALID_RSS = "invalid_rss", "Invalid RSS"
        NOT_MODIFIED = "not_modified", "Not Modified"
        UNAVAILABLE = "unavailable", "Unavailable"

    rss = models.URLField(unique=True, max_length=500)

    active = models.BooleanField(
        default=True,
        help_text="Inactive podcasts will no longer be updated from their RSS feeds.",
    )

    private = models.BooleanField(
        default=False,
        help_text="Only available to subscribers",
    )

    etag = models.TextField(blank=True)
    title = models.TextField(blank=True)

    pub_date = models.DateTimeField(null=True, blank=True)

    parsed = models.DateTimeField(null=True, blank=True)

    parser_error = models.CharField(
        max_length=30, choices=ParserError.choices, blank=True
    )

    frequency = models.DurationField(null=True, blank=True)

    modified = models.DateTimeField(
        null=True,
        blank=True,
    )

    content_hash = models.CharField(max_length=64, blank=True)

    num_retries = models.PositiveSmallIntegerField(default=0)

    cover_url = models.URLField(max_length=2083, blank=True)

    funding_url = models.URLField(max_length=2083, blank=True)
    funding_text = models.TextField(blank=True)

    language = models.CharField(
        max_length=2,
        default="en",
        validators=[MinLengthValidator(2)],
    )

    description = models.TextField(blank=True)
    website = models.URLField(max_length=2083, blank=True)
    keywords = models.TextField(blank=True)
    extracted_text = models.TextField(blank=True)
    owner = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(
        auto_now=True, verbose_name="Podcast Updated in Database"
    )

    explicit = models.BooleanField(default=False)
    promoted = models.BooleanField(default=False)

    categories: models.QuerySet[Category] = models.ManyToManyField(
        "podcasts.Category",
        blank=True,
        related_name="podcasts",
    )

    recipients: models.QuerySet[User] = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="recommended_podcasts",
    )

    search_vector = SearchVectorField(null=True, editable=False)

    objects: models.Manager[Podcast] = PodcastQuerySet.as_manager()

    class Meta:
        indexes: ClassVar[list] = [
            models.Index(fields=["-pub_date"]),
            models.Index(fields=["pub_date"]),
            models.Index(fields=["promoted"]),
            models.Index(fields=["content_hash"]),
            models.Index(
                models.functions.Lower("title"),
                name="%(app_label)s_%(class)s_lwr_title_idx",
            ),
            GinIndex(fields=["search_vector"]),
        ]

    def __str__(self) -> str:
        """Returns podcast title or RSS if missing."""
        return self.title or self.rss

    def get_absolute_url(self) -> str:
        """Default absolute URL of podcast."""
        return self.get_detail_url()

    def get_detail_url(self) -> str:
        """Absolute URL of podcast detail page."""
        return reverse(
            "podcasts:podcast_detail",
            kwargs={
                "podcast_id": self.pk,
                "slug": self.slug,
            },
        )

    def get_episodes_url(self) -> str:
        """URL of podcast episode list page."""
        return reverse(
            "podcasts:episodes",
            kwargs={
                "podcast_id": self.pk,
                "slug": self.slug,
            },
        )

    def get_similar_url(self) -> str:
        """URL of podcast similar recommendations page."""
        return reverse(
            "podcasts:similar",
            kwargs={
                "podcast_id": self.pk,
                "slug": self.slug,
            },
        )

    def get_latest_episode_url(self) -> str:
        """URL of latest episode."""
        return reverse(
            "podcasts:latest_episode",
            kwargs={
                "podcast_id": self.pk,
            },
        )

    @cached_property
    def cleaned_title(self) -> str:
        """Strips HTML from title field."""
        return strip_html(self.title)

    @cached_property
    def cleaned_description(self) -> str:
        """Strips HTML from description field."""
        return strip_html(self.description)

    @cached_property
    def slug(self) -> str:
        """Returns slugified title."""
        return slugify(self.title, allow_unicode=False) or "no-title"

    @cached_property
    def num_episodes(self) -> int:
        """Returns number of episodes."""
        return self.episodes.count()

    @cached_property
    def has_similar(self) -> bool:
        """Returns true if any recommendations."""
        return False if self.private else self.recommendations.exists()


class Subscription(models.Model):
    """Subscribed podcast belonging to a user's collection."""

    subscriber: User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    podcast: Podcast = models.ForeignKey(
        "podcasts.Podcast",
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints: ClassVar[list] = [
            models.UniqueConstraint(
                name="unique_%(app_label)s_%(class)s_user_podcast",
                fields=["subscriber", "podcast"],
            )
        ]
        indexes: ClassVar[list] = [models.Index(fields=["-created"])]

    def __str__(self) -> str:
        """Required __str__ method"""
        return str(self._meta.verbose_name)


class RecommendationQuerySet(models.QuerySet):
    """Custom QuerySet for Recommendation model."""

    def with_relevance(self) -> models.QuerySet[Recommendation]:
        """Returns factor of frequency and similarity as annotated value `relevance`."""
        return self.annotate(relevance=models.F("frequency") * models.F("similarity"))

    def bulk_delete(self) -> int:
        """More efficient quick delete.

        Returns:
            number of rows deleted
        """
        return self._raw_delete(self.db)


class Recommendation(models.Model):
    """Recommendation based on similarity between two podcasts."""

    podcast: Podcast = models.ForeignKey(
        "podcasts.Podcast",
        on_delete=models.CASCADE,
        related_name="recommendations",
    )

    recommended: Podcast = models.ForeignKey(
        "podcasts.Podcast",
        on_delete=models.CASCADE,
        related_name="similar",
    )

    frequency = models.PositiveIntegerField(default=0)

    similarity = models.DecimalField(
        decimal_places=10,
        max_digits=100,
        null=True,
        blank=True,
    )

    objects: models.Manager[Recommendation] = RecommendationQuerySet.as_manager()

    class Meta:
        indexes: ClassVar[list] = [
            models.Index(fields=["podcast"]),
            models.Index(fields=["recommended"]),
            models.Index(fields=["-similarity", "-frequency"]),
        ]
        constraints: ClassVar[list] = [
            models.UniqueConstraint(
                name="unique_%(app_label)s_%(class)s",
                fields=["podcast", "recommended"],
            ),
        ]

    def __str__(self) -> str:
        """Returns ID of recommendation."""
        return f"Recommendation #{self.pk}"
