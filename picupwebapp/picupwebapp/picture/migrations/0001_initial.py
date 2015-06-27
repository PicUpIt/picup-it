# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=140)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('exif', models.BooleanField(default=False)),
                ('license', models.IntegerField(default=0, choices=[(0, b'Unknown'), (1, b'Copyright'), (2, b'Attribution CC BY'), (3, b'Attribution-ShareAlike CC BY-SA'), (4, b'Attribution-NoDerivs CC BY-ND'), (5, b'Attribution-NonCommercial CC BY-NC'), (6, b'Attribution-NonCommercial-ShareAlike CC BY-NC-SA'), (7, b'Attribution-NonCommercial-NoDerivs CC BY-NC-ND')])),
                ('user', models.ForeignKey(related_name='gallery', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'pictures')),
                ('picture_thumb', models.ImageField(upload_to=b'thumbs')),
                ('picture_medium', models.ImageField(upload_to=b'meds')),
                ('picture_smart', models.ImageField(upload_to=b'smarts')),
                ('created', models.DateTimeField(auto_now=True)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('gallery', models.ForeignKey(to='picture.Gallery', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PictureDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=140)),
                ('created', models.DateTimeField(auto_now=True)),
                ('picture', models.ForeignKey(related_query_name=b'desc', related_name='description', to='picture.Picture', unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='gallery',
            unique_together=set([('title', 'user')]),
        ),
    ]
