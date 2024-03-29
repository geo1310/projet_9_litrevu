# Generated by Django 5.0.2 on 2024-02-14 14:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookreview", "0004_alter_review_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(5),
                ],
                verbose_name="Note",
            ),
        ),
    ]
