from django.db.models import Count
from django.contrib.auth.models import User
from django.conf import settings 
from models import Gallery

RECOMMENDED_ROWS = settings.RECOMMENDED_ROWS

def get_recommended_all():
    """Get all recommened view.
    """
    return get_recommended(0,0)


def get_recommended(min_picture_gallery=2, min_picture_user=10, cc=True):
    """Get recommended galleries and users.
    
    Parameters
    ----------
    min_picture_gallery : int
    min_picture_user : int
    cc : bool
        Creative Commons bool"""
    galleries = Gallery.objects.all().order_by('title')
    galleries = galleries.annotate(num_pictures=Count('picture'))
    galleries = galleries.filter(num_pictures__gt=min_picture_gallery).order_by('-id')
    if cc:
        galleries = galleries.exclude(license__in=[0,1])
        
    users = User.objects.all().annotate(num_pictures=Count('picture')).filter(num_pictures__gt=min_picture_user).order_by('-id')
    
    number_galleries = ((galleries.count()/RECOMMENDED_ROWS)*RECOMMENDED_ROWS)
    if number_galleries<0:
        galleries=None
    else:
        galleries = galleries[0:number_galleries]

    number_users = ((users.count()/RECOMMENDED_ROWS)*RECOMMENDED_ROWS)
    if settings.DEBUG == True:
        number_users = 2
    if number_users<0:
        users=None
    else:
        users = users[0:number_users]
    return (galleries, users)

def serialize_picture(picture):
    """Serialize picture into json.
    
    Parameters
    ----------
    picture : Picture
    """
    picture_json = {}
    picture_json['id'] = picture.id
    try:
        picture_json['description'] = picture.description.all().first().text
    except AttributeError:
        picture_json['description'] = ''
    picture_json['thumb'] = picture.picture_thumb.url
    picture_json['medium'] = picture.picture_medium.url
    picture_json['picture'] = picture.picture.url
    return picture_json


def serialize_gallery(gallery, children=False):
    """Serialize gallery into json.
    
    Parameters
    ----------
    picture : Picture
    children : bool
    """    
    gallery_json = {}
    gallery_json['id'] = gallery.id
    gallery_json['user_id'] = gallery.user_id
    gallery_json['title'] = gallery.title
    gallery_json['thumb'] = gallery.picture_set.first().picture_thumb.url

    if children:
        pictures = gallery.picture_set.all()
        pictures_dict = [ serialize_picture(x) for x in pictures ]
        gallery_json['pictures'] = pictures_dict

    return gallery_json


def serialize_user(user, children=False):
    """Serialize picture into json.

    Parameters
    ----------
    picture : Picture
    children : bool
    """    
    user_json = {}
    user_json['id'] = user.id
    user_json['username'] = user.username
    user_json['thumb'] = user.picture_set.first().picture_thumb.url
    if children:
        pictures = user.picture_set.filter(gallery_id=None)
        pictures_dict = [ serialize_picture(x) for x in pictures ]
        user_json['pictures'] = pictures_dict
        galleries = Gallery.objects.filter(user=user)
        galleries_dict = [ serialize_gallery(x) for x in  galleries]
        user_json['galleries'] = galleries_dict
    return user_json


def get_recommended_filter(min_picture_gallery=2, min_picture_user=10, cc=True, filter_list=[]):
    """Alternative version of getting results.
    """
    galleries = Gallery.objects.all().order_by('title').annotate(num_pictures=Count('picture')).filter(num_pictures__gt=min_picture_gallery).order_by('-id')

    if cc:
        galleries = galleries.exclude(license__in=[0,1])

    users = User.objects.all().annotate(num_pictures=Count('picture')).filter(num_pictures__gt=min_picture_user).order_by('-id')

    if filter_list:
        galleries = galleries.filter(license__in=filter_list)

    if settings.DEBUG == True:
        number_users = 2
    else:
        number_users = 2

    if number_users<0:
        users=None
    else:
        users = users[0:number_users]

    return (galleries, users)