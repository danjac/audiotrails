# Generated by Django 4.0 on 2021-12-22 11:10

from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_autoplay"),
        ("episodes", "0022_episode_link"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Favorite",
            new_name="Bookmark",
        ),
        migrations.RemoveConstraint(
            model_name="bookmark",
            name="unique_episodes_favorite",
        ),
        migrations.RemoveIndex(
            model_name="bookmark",
            name="episodes_fa_created_edc79e_idx",
        ),
        migrations.AddIndex(
            model_name="bookmark",
            index=models.Index(
                fields=["-created"], name="episodes_bo_created_d69e08_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="bookmark",
            constraint=models.UniqueConstraint(
                fields=("user", "episode"), name="unique_episodes_bookmark"
            ),
        ),
    ]
