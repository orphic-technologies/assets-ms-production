# Generated by Django 4.1.3 on 2023-02-04 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0028_remove_vendor_vat_no"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assestreturn",
            name="asset_info",
        ),
        migrations.AddField(
            model_name="assestreturn",
            name="asset_code",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="assestreturn",
            name="asset_name",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
