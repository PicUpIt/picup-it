#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import os.path
from picupwebapp.picture.models  import Picture


class Command(BaseCommand):
    args = ''
    help = 'Update a single thumb'

    def handle(self, *args, **options):
        picture = Picture.objects.get(id=args[0])
        print "Converting picture %s" % picture.id
        picture.update_thumb()