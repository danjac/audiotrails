# Django
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVectorField,
    TrigramSimilarity,
)
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.text import slugify

# Third Party Libraries
from model_utils.models import TimeStampedModel
from PIL import ImageFile
from sorl.thumbnail import ImageField

from radiofeed.typing import AnyUser

ImageFile.LOAD_TRUNCATED_IMAGES = True


class CategoryQuerySet(models.QuerySet):
    def search(self, search_term: str, base_similarity=0.2) -> models.QuerySet:
        return self.annotate(
            similarity=TrigramSimilarity("name", force_str(search_term))
        ).filter(similarity__gte=base_similarity)


CategoryManager: models.Manager = models.Manager.from_queryset(CategoryQuerySet)


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    # https://itunes.apple.com/search?term=podcast&genreId=1402&limit=20
    itunes_genre_id = models.IntegerField(
        verbose_name="iTunes Genre ID", null=True, blank=True, unique=True
    )

    objects = CategoryManager()

    class Meta:
        verbose_name_plural = "categories"
        ordering = ("name",)

    def __str__(self):
        return self.name

    @property
    def slug(self) -> str:
        return slugify(self.name, allow_unicode=False)

    def get_absolute_url(self) -> str:
        return reverse("podcasts:category_detail", args=[self.id, self.slug])


class PodcastQuerySet(models.QuerySet):
    def search(self, search_term: str) -> models.QuerySet:
        if not search_term:
            return self.none()

        query = SearchQuery(force_str(search_term), search_type="websearch")
        return self.annotate(
            rank=SearchRank(models.F("search_vector"), query=query)
        ).filter(search_vector=query)

    def with_subscription_count(self) -> models.QuerySet:
        return self.annotate(subscription_count=models.Count("subscription"))


PodcastManager: models.Manager = models.Manager.from_queryset(PodcastQuerySet)


class Podcast(models.Model):

    rss = models.URLField(unique=True, max_length=500)
    etag = models.TextField(blank=True)
    title = models.TextField()
    pub_date = models.DateTimeField(null=True, blank=True)

    cover_image = ImageField(null=True, blank=True)

    itunes = models.URLField(max_length=500, null=True, blank=True, unique=True)

    language = models.CharField(max_length=2, default="en")
    description = models.TextField(blank=True)
    link = models.URLField(null=True, blank=True, max_length=500)
    keywords = models.TextField(blank=True)
    extracted_text = models.TextField(blank=True)
    authors = models.TextField(blank=True)

    last_updated = models.DateTimeField(null=True, blank=True)

    explicit: bool = models.BooleanField(default=False)
    promoted = models.BooleanField(default=False)

    categories = models.ManyToManyField(Category, blank=True)

    # received recommendation email
    recipients = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="recommended_podcasts"
    )

    sync_error = models.TextField(blank=True)
    num_retries = models.PositiveIntegerField(default=0)

    search_vector = SearchVectorField(null=True, editable=False)

    objects = PodcastManager()

    class Meta:
        indexes = [
            models.Index(fields=["-pub_date"]),
            models.Index(fields=["pub_date"]),
            GinIndex(fields=["search_vector"]),
        ]

    def __str__(self) -> str:
        return self.title or self.rss

    def get_absolute_url(self) -> str:
        return reverse("podcasts:podcast_episode_list", args=[self.id, self.slug])

    @property
    def slug(self) -> str:
        return slugify(self.title, allow_unicode=False) or "podcast"

    def get_subscribe_toggle_id(self) -> str:
        # https://github.com/hotwired/turbo/issues/86
        return f"podcast-subscribe-{self.id}"


class Subscription(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="uniq_subscription", fields=["user", "podcast"]
            )
        ]
        indexes = [models.Index(fields=["-created"])]


class RecommendationQuerySet(models.QuerySet):
    def with_subscribed(self, user: AnyUser) -> models.QuerySet:
        """Marks which recommendations are subscribed by this user."""
        if user.is_anonymous:
            return self.annotate(
                is_subscribed=models.Value(False, output_field=models.BooleanField())
            )
        return self.annotate(
            is_subscribed=models.Exists(
                Subscription.objects.filter(
                    user=user, podcast=models.OuterRef("recommended")
                )
            )
        )

    def for_user(self, user: settings.AUTH_USER_MODEL) -> models.QuerySet:
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
            | set(user.subscription_set.values_list("podcast", flat=True))
        )

        return self.filter(podcast__pk__in=podcast_ids).exclude(
            recommended__pk__in=podcast_ids
            | set(user.recommended_podcasts.values_list("pk", flat=True))
        )


RecommendationManager: models.Manager = models.Manager.from_queryset(
    RecommendationQuerySet
)


class Recommendation(models.Model):
    podcast = models.ForeignKey(Podcast, related_name="+", on_delete=models.CASCADE)
    recommended = models.ForeignKey(Podcast, related_name="+", on_delete=models.CASCADE)

    frequency = models.PositiveIntegerField(default=0)

    similarity = models.DecimalField(
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
