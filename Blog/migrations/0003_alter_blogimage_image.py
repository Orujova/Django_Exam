# Generated by Django 4.2.2 on 2023-06-27 20:03

import Blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_blog_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogimage',
            name='image',
            field=models.ImageField(upload_to=Blog.models.upload_image),
        ),
    ]
