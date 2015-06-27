#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Image processing tools.
"""

from unidecode import unidecode
from django.conf import settings
import StringIO
try:
    from PIL import Image, ImageOps, ImageFilter
except ImportError:
    import Image
    import ImageOps
import os.path
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
import pyexiv2

THUMB_SIZE =  settings.PICUP_THUMB_SIZE
MEDIUM_SIZE =  settings.PICUP_MEDIUM_SIZE

def rotate_picture(picture):
    """Detect if picture should be rotated.
    
    Parameters
    ----------
    picture : Picture
    """
    tags = {}
    i = Image.open(picture.picture.file)
 
    try:
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag,tag)
            tags[decoded] = value
        orientation = tags['Orientation']
    except:
        orientation = 1
    if not orientation==1:
        orig_filename = picture.picture.file.name+'.orig'
        file_ext = picture.picture.file.name.split('.')[-1]
        new_filename = picture.picture.file.name+'_fix.'+file_ext
        if not os.path.exists(orig_filename):
            shutil.copyfile(picture.picture.file.name, orig_filename)
        exif_orig = pyexiv2.ImageMetadata(picture.picture.file.name)
        exif_orig.read()
        i = Image.open(orig_filename)
        if orientation == 3:   
            i = i.transpose(Image.ROTATE_180)
        elif orientation == 6: 
            i = i.transpose(Image.ROTATE_270)
        elif orientation == 8: 
            i = i.transpose(Image.ROTATE_90)
        i.save(picture.picture.file.name)
        exif_new = pyexiv2.ImageMetadata(picture.picture.file.name)
        exif_new.read()
        exif_orig.copy(exif_new)
        exif_new['Exif.Image.Orientation'] = 1
        exif_new.write()
        picture.update_thumb()

def process_image(image, size_x, size_y):
    """Process an image.
    
    Parameters
    ----------
    image: models.ImageField
    size_x : int
        width of the image
    size_y : int
        height of the image
    """
    image.seek(0)
    imagefile  = StringIO.StringIO(image.read())
    imageImage = Image.open(imagefile)
    if imageImage.mode != "RGB":
        imageImage = imageImage.convert("RGB")

    size = imageImage.size

    resizedImage = ImageOps.fit(imageImage, (size_x, size_y), Image.ANTIALIAS)
    if size[0] < size_x or size[1] < size_y:
        if size[0] < size_x:
            posX =  (size_x-size[0])/2
        else:
            posX = 0
        if size[1] < size_y:
            posY =  (size_y-size[1])/2
        else:
            posY = 0
        resizedImage = resizedImage.filter(ImageFilter.SMOOTH)
        resizedImage = resizedImage.filter(ImageFilter.SMOOTH_MORE)
        resizedImage = resizedImage.filter(ImageFilter.BLUR)

    imagefile = StringIO.StringIO()
    resizedImage.save(imagefile,'JPEG')
    imagefile.seek(0)
    return imagefile

def image_smart(image, x, y):
    """Process an image.
    
    Parameters
    ----------
    image : models.ImageField
    x : int
        width of the image
    y : int
        height of the image
    """    
    return process_image(image, x, y)

def image_medium(image):
    """Process an image with MEDIUM_SIZE as size.
    
    Parameters
    ----------
    image : models.ImageField
    """
    return process_image(image, MEDIUM_SIZE[0], MEDIUM_SIZE[1])
    

def image_thumb(image):
    """Process an image with THUMB_SIZE as size.
    
    Parameters
    ----------
    image : models.ImageField
    """    
    return process_image(image, THUMB_SIZE[0], THUMB_SIZE[1])

def get_metadata(filename):
    """Get metadata from the image file.
    
    Parameters
    ----------
    filename : str
    """
    metadata = pyexiv2.ImageMetadata(filename)
    metadata.read()
    return metadata




