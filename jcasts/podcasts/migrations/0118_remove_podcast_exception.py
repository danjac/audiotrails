# Generated by Django 4.0 on 2021-12-13 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("podcasts", "0117_podcast_content_hash"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="podcast",
            name="exception",
        ),
    ]
