import os.path
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from django.core.management.base import BaseCommand, CommandError
from picupwebapp.picture.models  import Picture

class Command(BaseCommand):
    args = ''
    help = 'Show EXIF TAGS for the pictures'

    def handle(self, *args, **options):
        pictures = Picture.objects.all()

        for picture in pictures:
            ret = {}
            #print "Checking picture %s" % picture.id
            i = Image.open(picture.picture.file)
            try:
                info = i._getexif()
                for tag, value in info.items():
                    decoded = TAGS.get(tag,tag)
                    ret[decoded] = value
                    orientation = ret['Orientation']
            except AttributeError:
                    orientation = 1
            except KeyError:
                    orientation = 1
                    print ret.keys()
            
            if not orientation==1:
                print 'ID: %s Orientation: %s Model: %s Software %s' % (picture.id, ret['Orientation'], ret['Model'], ret['Software'])
