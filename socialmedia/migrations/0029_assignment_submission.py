# Generated by Django 4.2.1 on 2023-11-02 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("socialmedia", "0028_post_allow_replies"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="assignments/images/"
                    ),
                ),
                (
                    "video_upload",
                    models.FileField(
                        blank=True, null=True, upload_to="assignments/videos/"
                    ),
                ),
                (
                    "file_upload",
                    models.FileField(
                        blank=True, null=True, upload_to="assignments/files/"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "unit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="socialmedia.unit",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="submissions/images/"
                    ),
                ),
                (
                    "video_upload",
                    models.FileField(
                        blank=True, null=True, upload_to="submissions/videos/"
                    ),
                ),
                (
                    "file_upload",
                    models.FileField(
                        blank=True, null=True, upload_to="submissions/files/"
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("is_approved", models.BooleanField(default=False)),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="socialmedia.assignment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-timestamp"],
            },
        ),
    ]
