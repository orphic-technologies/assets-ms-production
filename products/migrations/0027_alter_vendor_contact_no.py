# Generated by Django 4.1.3 on 2023-01-26 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0026_alter_product_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendor",
            name="contact_no",
            field=models.CharField(max_length=50),
        ),
    ]
