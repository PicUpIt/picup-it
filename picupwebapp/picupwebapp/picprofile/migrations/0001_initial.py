# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('picture', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PicupProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('api_key', models.CharField(max_length=96)),
                ('newsletter', models.BooleanField(default=True)),
                ('karma', models.IntegerField(default=0)),
                ('profile_picture', models.ForeignKey(null=True, to='picture.Picture', unique=True)),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
