# Generated by Django 5.0.3 on 2024-04-03 10:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fact_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="invoice_date",
            field=models.DateField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Date",
            ),
            preserve_default=False,
        ),
    ]