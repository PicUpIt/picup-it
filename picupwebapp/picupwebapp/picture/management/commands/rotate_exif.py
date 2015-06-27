from django.core.management.base import BaseCommand, CommandError
from picupwebapp.picture.models  import Picture
from picupwebapp.picture.tools  import rotate_picture
class Command(BaseCommand):
    args = ''
    help = 'Rotate EXIF TAGS for the pictures'

    def handle(self, *args, **options):
        pictures = Picture.objects.all()
        for picture in pictures:
            rotate_picture(picture)