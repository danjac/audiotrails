# Generated by Django 3.2.9 on 2021-11-30 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("podcasts", "0107_auto_20211129_2007"),
    ]

    operations = [
        migrations.AddField(
            model_name="podcast",
            name="websub_callback_exception",
            field=models.TextField(blank=True),
        ),
    ]
