# Generated by Django 5.1.1 on 2024-09-21 08:18

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
