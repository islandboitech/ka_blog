# Generated by Django 4.2.4 on 2023-08-25 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creds', '0003_user_avatar_alter_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='Full Name'),
        ),
    ]
