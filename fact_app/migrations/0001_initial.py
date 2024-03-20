# Generated by Django 5.0.3 on 2024-03-20 16:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("name", models.CharField(max_length=132)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=130)),
                ("address", models.CharField(max_length=64)),
                (
                    "sex",
                    models.CharField(
                        choices=[("M", "Masculin"), ("F", "Feminin")], max_length=1
                    ),
                ),
                ("age", models.CharField(max_length=12)),
                ("city", models.CharField(max_length=33)),
                ("zip_code", models.CharField(max_length=16)),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                (
                    "save_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer",
                "verbose_name_plural": "Customers",
            },
        ),
        migrations.CreateModel(
            name="Invoice",
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
                ("invoice_date_time", models.DateTimeField(auto_now_add=True)),
                ("total", models.DecimalField(decimal_places=2, max_digits=10000)),
                ("last_updated_date", models.DateTimeField(blank=True, null=True)),
                ("paid", models.BooleanField(default=False)),
                (
                    "invoice_type",
                    models.CharField(
                        choices=[
                            ("R", "Reçu"),
                            ("P", "Proforma facture"),
                            ("F", "Facture"),
                        ],
                        max_length=1,
                    ),
                ),
                ("comments", models.TextField(blank=True, max_length=1000, null=True)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="fact_app.customer",
                    ),
                ),
                (
                    "save_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Invoice",
                "verbose_name_plural": "Invoices",
            },
        ),
        migrations.CreateModel(
            name="Article",
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
                ("name", models.CharField(max_length=150)),
                ("quantity", models.IntegerField()),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=1000)),
                ("total", models.DecimalField(decimal_places=2, max_digits=1000)),
                (
                    "save_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="fact_app.invoice",
                    ),
                ),
            ],
            options={
                "verbose_name": "Article",
                "verbose_name_plural": "Articles",
            },
        ),
    ]
