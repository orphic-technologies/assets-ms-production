# Generated by Django 4.1.3 on 2023-02-09 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0031_alter_assestreturn_expected_date_of_return_of_such_asset"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="updated_by",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
