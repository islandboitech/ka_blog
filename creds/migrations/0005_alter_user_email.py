# Generated by Django 4.2.4 on 2023-08-25 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creds', '0004_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='Email address'),
        ),
    ]
