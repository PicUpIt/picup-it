#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import os.path
from picupwebapp.picture.models  import Picture

class Command(BaseCommand):
    args = ''
    help = 'Update size width and height'

    def handle(self, *args, **options):
        pictures = Picture.objects.all().filter(width=0)
        for picture in pictures:
            try:
                x = picture.picture.width
                y = picture.picture.height
                picture.width = x
                picture.height = y
                picture.save()
                #print "ok ",x,y, picture
            except IOError:
                print "missing file:",picture 