# Generated by Django 3.2.16 on 2023-07-16 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0004_auto_20230716_1556"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="group",
        ),
        migrations.AddField(
            model_name="post",
            name="group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="posts.group",
                verbose_name="Группа",
            ),
        ),
    ]
