#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import os.path
from picupwebapp.picture.models  import Picture

class Command(BaseCommand):
    args = ''
    help = 'Update thumbs'

    def handle(self, *args, **options):
        pictures = Picture.objects.all()
        for picture in pictures:
            print "Converting picture %s" % picture.id
            picture.update_thumb()