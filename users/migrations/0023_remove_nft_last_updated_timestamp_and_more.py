# Generated by Django 4.2.1 on 2023-08-11 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0022_nft_last_updated_timestamp_nft_private_key_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="nft",
            name="last_updated_timestamp",
        ),
        migrations.RemoveField(
            model_name="nft",
            name="private_key",
        ),
        migrations.RemoveField(
            model_name="nft",
            name="wallet_address",
        ),
    ]
