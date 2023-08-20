# Generated by Django 4.2.4 on 2023-08-20 02:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_rename_athor_blog_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='paticipants',
            field=models.ManyToManyField(blank=True, related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]
