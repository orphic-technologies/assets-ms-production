# Generated by Django 4.1.3 on 2023-02-02 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0027_alter_vendor_contact_no"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vendor",
            name="vat_no",
        ),
    ]
