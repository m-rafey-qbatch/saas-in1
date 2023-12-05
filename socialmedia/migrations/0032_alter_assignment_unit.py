# Generated by Django 4.2.1 on 2023-11-06 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("socialmedia", "0031_assignment_due_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assignment",
            name="unit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assignments",
                to="socialmedia.unit",
            ),
        ),
    ]