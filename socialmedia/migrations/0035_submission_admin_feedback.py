# Generated by Django 4.2.1 on 2023-11-08 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("socialmedia", "0034_alter_post_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="submission",
            name="admin_feedback",
            field=models.TextField(blank=True, verbose_name="Admin Feedback"),
        ),
    ]
