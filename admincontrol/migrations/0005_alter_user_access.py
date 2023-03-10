# Generated by Django 4.1.3 on 2023-01-26 09:39

import admincontrol.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admincontrol", "0004_alter_user_current_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="access",
            field=models.CharField(
                choices=[
                    ("superadmin", "SUPERADMIN"),
                    ("user", "USER"),
                    ("staff", "STAFF"),
                ],
                default=admincontrol.models.PowerShare["USER"],
                max_length=50,
            ),
        ),
    ]
