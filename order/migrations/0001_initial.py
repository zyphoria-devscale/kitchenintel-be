# Generated by Django 5.2.1 on 2025-05-13 15:47

import django.core.validators
import django.db.models.deletion
import shared.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("menu", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                (
                    "status",
                    models.CharField(
                        choices=[("PAID", "Paid"), ("UNPAID", "Unpaid")],
                        default="UNPAID",
                        max_length=10,
                    ),
                ),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                (
                    "quantity",
                    models.IntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                (
                    "price_at_order_time",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=10)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "menu_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="menu.menu"
                    ),
                ),
                (
                    "order_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="order.order"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="order",
            name="order_items",
            field=models.ManyToManyField(through="order.OrderItem", to="menu.menu"),
        ),
    ]
