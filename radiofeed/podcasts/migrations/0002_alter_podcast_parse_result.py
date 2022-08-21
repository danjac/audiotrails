# Generated by Django 4.0.6 on 2022-07-18 11:44

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "podcasts",
            "0001_squashed_0150_remove_subscription_unique_podcasts_subscription_user_podcast_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="podcast",
            name="parse_result",
            field=models.CharField(
                blank=True,
                choices=[
                    ("success", "Success"),
                    ("complete", "Complete"),
                    ("not_modified", "Not Modified"),
                    ("http_error", "HTTP Error"),
                    ("rss_parser_error", "RSS Parser Error"),
                    ("duplicate_feed", "Duplicate Feed"),
                ],
                max_length=30,
                null=True,
                verbose_name="Feed Update Result",
            ),
        ),
    ]
