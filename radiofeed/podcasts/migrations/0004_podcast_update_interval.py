# Generated by Django 4.0.6 on 2022-07-30 20:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0003_alter_podcast_http_status_alter_podcast_num_retries'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='update_interval',
            field=models.DurationField(default=datetime.timedelta(days=1), verbose_name='Update Interval'),
        ),
    ]
