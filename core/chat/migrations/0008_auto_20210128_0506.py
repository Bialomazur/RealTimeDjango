# Generated by Django 3.0.5 on 2021-01-28 04:06

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20210128_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='chat_hash',
            field=models.TextField(default=chat.models.generate_socket_hash, max_length=32, unique=True),
        ),
    ]
