# Generated by Django 4.2.4 on 2023-08-26 05:33

import creds.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creds', '0005_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.png', null=True, upload_to=creds.models.user_directory_path, verbose_name='Profile piture'),
        ),
    ]
