# Generated by Django 5.0.6 on 2024-10-19 06:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AJKapp', '0011_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='postcreated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
