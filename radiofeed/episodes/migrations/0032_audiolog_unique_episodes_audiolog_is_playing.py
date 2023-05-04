# Generated by Django 4.1.7 on 2023-03-04 10:11


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("episodes", "0031_audiolog_is_playing"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="audiolog",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_playing", True)),
                fields=("user", "is_playing"),
                name="unique_episodes_audiolog_is_playing",
            ),
        ),
    ]
