# Generated by Django 4.2.2 on 2023-06-20 17:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("podcasts", "0052_remove_podcast_queued"),
    ]

    operations = [
        migrations.RenameField(
            model_name="podcast",
            old_name="link",
            new_name="website",
        ),
    ]
