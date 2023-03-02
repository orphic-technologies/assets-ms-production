# Generated by Django 4.1.3 on 2023-02-27 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0032_product_updated_by"),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
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
                ("location_name", models.CharField(max_length=100)),
            ],
        ),
    ]
