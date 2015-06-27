#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import os.path

from picupwebapp.picture import rabbit
from picupwebapp.picprofile.models  import PicupProfile

from picupwebapp.picture.models  import Picture, Gallery
from django.contrib.auth.models import User
import json
import pika



class Command(BaseCommand):
    args = ''
    help = 'Pull info from the queue and removes users'

    def callback(self,  ch, method, properties, body): 
        print body
        message = json.loads(body)
        print message
        user_id = message['user_id']

        user = User.objects.filter(id=user_id)
        print "got user ", user
        picup_profile = PicupProfile.objects.filter(user=user)

        pictures = Picture.objects.filter(user=user)
        galleries = Gallery.objects.filter(user=user)
        print user, picup_profile, pictures, galleries

        for picture in pictures:
            pass
            picture.picture.delete()
            picture.picture_thumb.delete()
            picture.picture_smart.delete()
            picture.picture_medium.delete()
            picture.delete()

        for gallery in galleries:
            gallery.delete()
        picup_profile.delete()
        print 
        user.delete()

        print " [x] Removed %r" % (body,)

    def handle(self, *args, **options):
        channel = rabbit.get_rabbit_channel()
        channel.queue_declare(queue='picup_remove')
        channel.basic_consume(self.callback,queue='picup_remove',no_ack=True)
        try:
            channel.start_consuming()
        except pika.exceptions.ConnectionClosed:
            print "Checked error"
        #channel.basic_consume(callback,queue='picup_remove',no_ack=True)
        print "checked"
        

        