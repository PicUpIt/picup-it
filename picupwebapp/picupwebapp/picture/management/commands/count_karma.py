#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import os.path

class Command(BaseCommand):
    args = ''
    help = 'Count karma'

    def handle(self, *args, **options):
        from picupwebapp.picture.models  import Picture
        from picupwebapp.picprofile.models  import PicupProfile, get_or_create_profile
        from django.contrib.auth.models import User

        users = User.objects.all()

        karma_all = {}
        for user in users:
            picup_profile = get_or_create_profile(user)
            karma = 0
            number_of_pictures = Picture.objects.filter(user=user).count()
            karma += number_of_pictures * 5
            number_of_pictures_galleries = Picture.objects.filter(user=user).exclude(gallery=None).count()
            karma += number_of_pictures_galleries * 1

            if user.id < 10:
                karma += 200
            elif user.id < 20:
                karma += 100
            elif user.id < 100:
                karma += 50
            elif user.id < 1000:
                karma += 25

            print user.email, number_of_pictures, number_of_pictures_galleries
            karma_all[user.id]  = {'username':user.email, 'points':karma}
            picup_profile.karma = karma
            picup_profile.save()
        print karma_all

