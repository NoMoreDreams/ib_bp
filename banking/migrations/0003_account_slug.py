# Generated by Django 4.2 on 2023-05-14 19:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("banking", "0002_rename_date_transaction_created_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="slug",
            field=models.SlugField(default=""),
        ),
    ]
