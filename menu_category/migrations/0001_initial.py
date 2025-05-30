# Generated by Django 5.2.1 on 2025-05-13 11:53

import django.db.models.deletion
import shared.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MenuCategory",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=shared.utils.generate_id,
                        editable=False,
                        max_length=100,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "parent_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="menu_category.menucategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Menu Category",
                "verbose_name_plural": "Menu Categories",
                "db_table": "menu_categories",
            },
        ),
    ]
