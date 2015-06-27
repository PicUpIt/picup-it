#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

from tools import image_thumb, image_medium, image_smart
from django.contrib.auth import get_user_model
import hashlib

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except:
    from django.contrib.auth.models import User  

from django.core.files.base import ContentFile

import json
from django.core.urlresolvers import reverse

CHOICES_LICENSE = (
    (0, 'Unknown'),
    (1, 'Copyright'),
    (2, 'Attribution CC BY'),
    (3, 'Attribution-ShareAlike CC BY-SA'),
    (4, 'Attribution-NoDerivs CC BY-ND'),
    (5, 'Attribution-NonCommercial CC BY-NC'),
    (6, 'Attribution-NonCommercial-ShareAlike CC BY-NC-SA'),
    (7, 'Attribution-NonCommercial-NoDerivs CC BY-NC-ND'),
)

DESCRIPTION_LICENSE = {
    0:  (""""Unknown""", None),
    1:  ("""All rights reserved""", None),
    2:  ("""This license lets others distribute, remix, tweak, and build upon your work, even commercially, as long as they credit you for the original creation. This is the most accommodating of licenses offered. Recommended for maximum dissemination and use of licensed materials. """, "ccby.png"),
    3:  ("""This license lets others remix, tweak, and build upon your work even for commercial purposes, as long as they credit you and license their new creations under the identical terms. This license is often compared to “copyleft” free and open source software licenses. All new works based on yours will carry the same license, so any derivatives will also allow commercial use. This is the license used by Wikipedia, and is recommended for materials that would benefit from incorporating content from Wikipedia and similarly licensed projects. """),
    4:  ("""This license allows for redistribution, commercial and non-commercial, as long as it is passed along unchanged and in whole, with credit to you. """),
    5:  ("""This license lets others remix, tweak, and build upon your work non-commercially, and although their new works must also acknowledge you and be non-commercial, they don’t have to license their derivative works on the same terms. """),
    6:  ("""This license lets others remix, tweak, and build upon your work non-commercially, as long as they credit you and license their new creations under the identical terms."""),
    7:  ("""This license is the most restrictive of our six main licenses, only allowing others to download your works and share them with others as long as they credit you, but they can’t change them in any way or use them commercially. """),
}

license_choices_files = ['unknown.png', 'copyright.png', 'ccby.png',  'ccbysa.png',  'ccbynd.png',  'ccbync.png',  'ccbyncsa.png',  'ccbyncnd.png'];
license_links = ['', '', 'by',  'by-sa',  'by-nd',  'by-nc',  'by-nc-sa',  'by-nc-nd'];

class Gallery(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="gallery")
    exif = models.BooleanField(default=False)
    license = models.IntegerField(default=0, choices=CHOICES_LICENSE)
    class Meta:
        unique_together = (('title', 'user',))

    def get_license_name(self):
        return CHOICES_LICENSE[self.license][1]

    def get_license_url(self):
        return 'https://creativecommons.org/licenses/'+license_links[self.license]+'/4.0/'

    def get_license_picture(self):
        return 'images/cc/%s' % license_choices_files[self.license]

    def get_absolute_url(self):
        return reverse('picupwebapp.picture.views.user_gallery', args=[str(self.user.id),str(self.id)])

    def get_json(self):
        object = {}
        object['id'] = self.id
        object['title'] = self.title
        object['description'] = self.description
        return json.dumps(object)

    def __str__(self):
        return "< PicUp Gallery Object <<%s / %s %s>>" % (self.id, self.user.id, self.user.username)

class Picture(models.Model):
    """Picture class.
    """
    user = models.ForeignKey(User)
    picture = models.ImageField(upload_to='pictures')
    picture_thumb = models.ImageField(upload_to='thumbs')
    picture_medium = models.ImageField(upload_to='meds')
    picture_smart = models.ImageField(upload_to='smarts')
    gallery = models.ForeignKey(Gallery, null=True)
    created = models.DateTimeField(auto_now=True)

    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('picupwebapp.picture.views.picture_view', args=[str(self.id)])

    def get_mime_type(self):
        """Get a mime type - used by Dublin Core parts.
        """
        try:
            stype = str(self.picture).split('.')[1]
        except:
            stype = ''
        mtype = stype if not 'jpg' else 'jpeg'
        return 'image/%s' % mtype

    def create_smart(self):
        """Create smart miniature.
        """
        width = self.picture.width
        height = self.picture.height
        ratio = min(640.0/width, 640.0/height)
        field_smart = getattr(self, 'picture_smart')
        self.picture.open()
        self.picture.seek(0)
        smart = image_smart(self.picture, int(width*ratio), int(height*ratio))
        smart_filename = hashlib.md5(smart.getvalue()).hexdigest()+'.jpg'
        field_smart.save(smart_filename, ContentFile(smart.read()))
    
    def is_cc(self):
        """Check if picture is Creative Commons.
        """
        if not self.gallery:
            return False
        return self.gallery.license>1

    def get_license_url(self):
        """Get the license url.
        """
        if self.gallery and self.gallery.license>1:
            return self.gallery.get_license_url()
        else:
            return ''

    def update_thumb(self):
        """Update the thumbnail.
        """
        if self.picture:
            # THUMBS
            field_thumb = getattr(self, 'picture_thumb')
            self.picture.open()
            self.picture.seek(0)
            thumb = image_thumb(self.picture)
            thumb_filename = hashlib.md5(thumb.getvalue()).hexdigest()+'.jpg'
            field_thumb.save(thumb_filename, ContentFile(thumb.read()))
            # MEDS
            field_medium = getattr(self, 'picture_medium')
            self.picture.open()
            self.picture.seek(0)
            medium = image_medium(self.picture)
            medium_filename = hashlib.md5(medium.getvalue()).hexdigest()+'.jpg'
            field_medium.save(medium_filename, ContentFile(medium.read()))
            self.create_smart()

    def is_gif(self):
        """Check if picture is a gif.
        """
        if self.picture.url.endswith('.gif'):
            return True
        else:
            return False

    def __str__(self):
        return 'Picture %s' % self.id

class BannerPictureDescriptionManager(models.Manager):
    def get_queryset(self):
        return super(BannerPictureDescriptionManager, self).get_queryset().filter(picture__gallery__license__gt=2).filter(picture__width__gt=1600).filter(picture__width__gt=1600)

class PictureDescription(models.Model):
    text = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now=True)
    picture = models.ForeignKey('Picture', null=False,unique=True,
        related_name="description", related_query_name="desc")

    objects = models.Manager()
    banners_objects = BannerPictureDescriptionManager()

def create_gallery(title, description, user):
    """Create the gallery.
    
    Parameters
    ----------
    title : str
    description : str 
    user : User
    """
    gallery = Gallery(title=title,
        description=description,
        user=user)
    gallery.save()
    return gallery

def get_user_galleries(user, as_json=True):
    galleries = Gallery.objects.filter(user=user)

    if as_json:
        return [ gallery.get_json() for gallery in galleries ]
    return galleries

def gallery_insert_picture(gallery, picture):
    if gallery.user.id == picture.user.id:
        picture.gallery = gallery
        picture.save()

def gallery_remove_picture(gallery, picture):
    """TODO: Should be implemented one day ;).
    """
    pass
