# Generated by Django 3.2.8 on 2021-10-08 07:24

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("podcasts", "0058_auto_20211008_0605"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="podcast",
            name="podcasts_po_pub_dat_38d2cb_idx",
        ),
        migrations.AddField(
            model_name="podcast",
            name="changed",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name="podcast",
            index=models.Index(
                fields=["-changed", "-pub_date"], name="podcasts_po_changed_2e38d6_idx"
            ),
        ),
    ]
