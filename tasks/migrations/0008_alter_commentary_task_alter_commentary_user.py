# Generated by Django 5.0.6 on 2024-05-21 10:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0007_alter_task_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commentary",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="commentaries",
                to="tasks.task",
            ),
        ),
        migrations.AlterField(
            model_name="commentary",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="commentaries",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
