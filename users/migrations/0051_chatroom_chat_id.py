# Generated by Django 4.2.1 on 2023-10-31 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0050_chatroom_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatroom",
            name="chat_id",
            field=models.CharField(
                default="default_chat_id", max_length=255, unique=True
            ),
            preserve_default=False,
        ),
    ]
