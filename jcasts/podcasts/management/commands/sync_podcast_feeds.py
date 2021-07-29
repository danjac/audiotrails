from django.core.management.base import BaseCommand

from jcasts.podcasts import scheduler


class Command(BaseCommand):
    help = "Run podcast feed updates"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--sporadic", action="store_true", help="Run less frequent podcast feeds"
        )

    def handle(self, *args, **options) -> None:
        if options["sporadic"]:
            num_feeds = scheduler.sync_sporadic_feeds()
        else:
            num_feeds = scheduler.sync_frequent_feeds()

        self.stdout.write(f"{num_feeds} feed(s) to be pulled")
