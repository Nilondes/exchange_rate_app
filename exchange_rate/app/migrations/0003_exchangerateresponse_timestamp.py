# Generated by Django 5.1.2 on 2024-10-30 12:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_exchangerateresponse_user_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchangerateresponse',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]