from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from jcasts.podcasts.feed_parser import calc_frequency
from jcasts.podcasts.models import Podcast


class Command(BaseCommand):
    help = "One-off command to (re)set starting frequencies for all relevant podcasts"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--reset", action="store_true", help="Reset all frequencies"
        )

    def handle(self, *args, **options) -> None:
        qs = Podcast.objects.filter(
            active=True,
            pub_date__isnull=False,
            pub_date__gte=timezone.now() - settings.RELEVANCY_THRESHOLD,
        ).order_by("-pub_date")

        if not options["reset"]:
            qs = qs.filter(frequency__isnull=True)

        total = qs.count()

        for counter, podcast in enumerate(qs.iterator(), 1):
            self.handle_podcast(podcast, counter, total)

    def handle_podcast(self, podcast, counter, total):
        pub_dates = (
            podcast.episode_set.filter(pub_date__lte=timezone.now())
            .values_list("pub_date", flat=True)
            .order_by("-pub_date")
        )
        frequency = calc_frequency(pub_dates)
        Podcast.objects.filter(pk=podcast.id).update(frequency=frequency)
        self.stdout.write(
            f"[{counter}/{total}] Podcast {podcast}: freq {frequency.days if frequency else 'None'}"
        )
