#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import os.path
from picupwebapp.picture.models  import Picture

class Command(BaseCommand):
    args = ''
    help = 'Create smart'

    def handle(self, *args, **options):
        if len(args)>0:
        	pictures = Picture.objects.filter(id__gte=args[0])
        else:
        	pictures = Picture.objects.all()
    	pictures = pictures.order_by('id')
        for picture in pictures:
            print "Smarting picture %s" % picture.id
            picture.create_smart()
            print