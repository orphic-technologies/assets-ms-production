# Generated by Django 4.1.3 on 2023-01-19 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_remove_assestassign_position_of_verified_authority"),
    ]

    operations = [
        migrations.AddField(
            model_name="assestassign",
            name="token",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
