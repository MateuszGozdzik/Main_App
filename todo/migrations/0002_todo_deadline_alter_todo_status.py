# Generated by Django 4.2 on 2023-04-22 12:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo",
            name="deadline",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="todo",
            name="status",
            field=models.CharField(
                choices=[
                    ("N", "Not Doing"),
                    ("D", "Doing"),
                    ("W", "Waiting"),
                    ("P", "Preparing"),
                    ("C", "Completed"),
                ],
                default="N",
                max_length=5,
            ),
        ),
    ]