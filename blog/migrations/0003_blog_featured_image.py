# Generated by Django 4.2.4 on 2023-08-25 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='featured_image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Featured image'),
        ),
    ]
