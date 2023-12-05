# Generated by Django 4.2.1 on 2023-09-29 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("webcamrecognition", "0002_webcamsession_face_recognized"),
    ]

    operations = [
        migrations.AddField(
            model_name="webcamsession",
            name="recognized_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sessions_recognized",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="webcamsession",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sessions_initiated",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]