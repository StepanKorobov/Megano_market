# Generated by Django 4.2.7 on 2024-10-14 18:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("goods", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrdersData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("fullName", models.CharField(blank=True, max_length=100, null=True)),
                ("email", models.EmailField(blank=True, max_length=100, null=True)),
                ("phone", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "deliveryType",
                    models.CharField(
                        blank=True, default="ordinary", max_length=100, null=True
                    ),
                ),
                (
                    "paymentType",
                    models.CharField(
                        blank=True, default="online", max_length=100, null=True
                    ),
                ),
                (
                    "totalCost",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("status", models.CharField(blank=True, max_length=16, null=True)),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("products", models.JSONField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("count", models.IntegerField(default=0)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order",
                        to="goods.product",
                    ),
                ),
            ],
        ),
    ]
