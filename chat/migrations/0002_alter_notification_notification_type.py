# Generated by Django 5.1.5 on 2025-02-07 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="notification_type",
            field=models.CharField(
                choices=[
                    ("join_request", "Join Request"),
                    ("group_report", "Group Report"),
                    ("chat_request", "Chat Request"),
                    ("mobile_request", "Mobile Request"),
                ],
                max_length=20,
            ),
        ),
    ]
