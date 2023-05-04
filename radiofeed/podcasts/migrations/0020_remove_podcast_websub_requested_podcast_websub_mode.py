# Generated by Django 4.1.6 on 2023-02-10 10:48


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("podcasts", "0019_remove_podcast_websub_verified"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="podcast",
            name="websub_requested",
        ),
        migrations.AddField(
            model_name="podcast",
            name="websub_mode",
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
