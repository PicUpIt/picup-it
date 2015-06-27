#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import os.path

from picupwebapp.picture import tools

def new_filename(filename):
    return os.path.join('/tmp', os.path.basename(filename))

class Command(BaseCommand):
    args = '<picture picture>'
    help = 'Converts the picture and save in tmp'

    def handle(self, *args, **options):
        for filename in args:
            new_f = new_filename(filename)
            print new_f
            thumb = tools.image_thumb(open(filename))
            new_fd = open(new_f, 'w')
            print type(thumb)
            #from ipdb import set_trace;set_trace()
            new_fd.write(thumb.read())
