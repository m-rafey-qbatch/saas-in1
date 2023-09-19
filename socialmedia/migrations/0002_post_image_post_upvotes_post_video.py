# Generated by Django 4.2.1 on 2023-09-18 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socialmedia", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="post_images/"),
        ),
        migrations.AddField(
            model_name="post",
            name="upvotes",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="post",
            name="video",
            field=models.FileField(blank=True, null=True, upload_to="post_videos/"),
        ),
    ]
