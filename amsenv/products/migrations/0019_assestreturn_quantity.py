# Generated by Django 4.1.3 on 2023-01-23 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0018_assestreturn"),
    ]

    operations = [
        migrations.AddField(
            model_name="assestreturn",
            name="quantity",
            field=models.IntegerField(blank=True, default=1),
        ),
    ]