# Generated by Django 4.1.3 on 2023-01-26 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admincontrol", "0006_alter_user_access"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]