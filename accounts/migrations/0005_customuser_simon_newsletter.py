# Generated by Django 4.2 on 2023-04-06 16:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_customuser_quote_newsletter"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="simon_newsletter",
            field=models.BooleanField(default=False),
        ),
    ]
