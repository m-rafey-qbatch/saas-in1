# Generated by Django 4.2.1 on 2023-10-23 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socialmedia", "0027_alter_post_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="allow_replies",
            field=models.BooleanField(default=True),
        ),
    ]
