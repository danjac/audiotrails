# Generated by Django 5.1.7 on 2025-03-10 14:29

from django.db import migrations


def _clear_duplicates(apps, schema_editor):
    Podcast = apps.get_model("podcasts", "Podcast")
    Podcast.objects.filter(parser_error="duplicate").update(
        active=True,
        parser_error="",
        num_retries=0,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("podcasts", "0020_podcast_canonical"),
    ]

    operations = [
        migrations.RunPython(
            _clear_duplicates,
            reverse_code=migrations.RunPython.noop,
        )
    ]
