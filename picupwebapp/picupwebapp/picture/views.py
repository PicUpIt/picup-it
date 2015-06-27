#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unidecode import unidecode
import collections
from random import randint 
import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.conf import settings
from django.db.models import Count

from django.views.decorators.clickjacking import xframe_options_exempt
from forms import UploadFileForm, GalleryLicenseForm
from models import Picture, PictureDescription, create_gallery, get_user_galleries, Gallery
from picupwebapp.picprofile.models import PicupProfile, get_or_create_profile

from tools import rotate_picture, get_metadata
from tools_views import get_recommended
from tools_views import get_recommended_all, serialize_picture
from tools_views import serialize_gallery, serialize_user
from picupwebapp.picprofile.tools import get_gravatar_url

import logging
logger = logging.getLogger(__name__)

from rabbit import get_rabbit_channel

from models import license_choices_files as license_choices
from models import CHOICES_LICENSE

from social.apps.django_app.utils import strategy
from social.actions import do_complete
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from social.strategies.utils import set_current_strategy_getter
from social.apps.django_app.utils import load_strategy
set_current_strategy_getter(load_strategy)

RECOMMENDED_ROWS = settings.RECOMMENDED_ROWS

@login_required
def deerbox_gallery(request,gallery_id):
    """User's gallery edit view.
    """
    try:
        gallery = Gallery.objects.get(user=request.user, id=gallery_id)
    except Gallery.DoesNotExist:
        raise Http404
    pictures_all = Picture.objects.filter(user=request.user,gallery_id=gallery_id)
    gravatar_url = get_gravatar_url(request.user.email)
    galleries = get_user_galleries(request.user,False)

    license_form = GalleryLicenseForm(instance=gallery)
    license_pic = license_choices[gallery.license]
    return render(request, 'deerbox_gallery.html', {'pictures_all':pictures_all,
        'gravatar_url':gravatar_url,
        'galleries':galleries,
        'gallery':gallery,
        'license_form':license_form,
        'license_pic':'images/cc/%s' % license_pic})

@xframe_options_exempt
@login_required
def accounts_profile(request):
    """User's profile edit view.
    """

    if request.GET.has_key('next'):
        if request.GET['next'] == 'ffos':
            return redirect('/mobile/ffoslogged/')        
        elif request.GET['next'] == 'ffosdata':
            return redirect('/mobile/data/')

    pictures_all = Picture.objects.filter(user=request.user,gallery=None)
    gravatar_url = get_gravatar_url(request.user.email)
    galleries = get_user_galleries(request.user,False)

    picup_profile = get_or_create_profile(request.user)

    return render(request, 'profile.html', {'pictures_all':pictures_all,
        'gravatar_url':gravatar_url,
        'galleries':galleries,
        'picup_profile':picup_profile})


def openid_pre(request):
    """OpenID login page view.
    """
    return render(request, "openid_pre.html", {})    

def user_gallery(request, user_id, gallery_id=None):
    """User's public user.
    
    Parameters
    ----------
    user_id : int
    gallery_id : int
    
    Note
    -----
    When gallery_id is None it servers user'r public profile page.
    """
    try:
        if int(user_id)==1:
            raise Http404
    except ValueError:
            raise Http404
    try:
        picup_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404

    picup_profile = get_or_create_profile(picup_user)

    pictures_all = Picture.objects.filter(user=picup_user).order_by('-created')
    if gallery_id:
        try:
            gallery =  Gallery.objects.get(id=gallery_id)
            pictures_all = pictures_all.filter(gallery=gallery).order_by('-created')
        except Gallery.DoesNotExist:
            raise Http404
    else:
        pictures_all = pictures_all.filter(gallery_id=None).order_by('-created')
        gallery = None
    pictures_clearing = pictures_all
    galleries = Gallery.objects.filter(user=picup_user).order_by('title').annotate(num_pictures=Count('picture')).filter(num_pictures__gt=0)
    user_gravatar_url = get_gravatar_url(picup_user.email)
    pictures_all_3 = pictures_all_2 = pictures_all_1 = None
    pictures_count = pictures_all.count()
    if pictures_all.count()<RECOMMENDED_ROWS:
        spare = pictures_all.count()
    else:
        spare = pictures_all.count() % RECOMMENDED_ROWS
    number_rows = pictures_all.count() / RECOMMENDED_ROWS

    if spare==3:
        pictures_all_3 = reversed(pictures_all[:3])
        pictures_all = pictures_all[3:number_rows*RECOMMENDED_ROWS+3]
    elif spare==2:
        pictures_all_2 = reversed(pictures_all[:2])
        pictures_all = pictures_all[2:number_rows*RECOMMENDED_ROWS+2]
    elif spare==1:
        pictures_all_1 = reversed(pictures_all[:1])
        pictures_all = pictures_all[1:number_rows*RECOMMENDED_ROWS+1]

    galleries_thumbs = galleries
    galleries_thumbs_3 = galleries_thumbs_2 = galleries_thumbs_1 = None

    if galleries.count()<RECOMMENDED_ROWS:
        spare = galleries.count()
    else:
        spare = galleries.count() % RECOMMENDED_ROWS
    number_rows = galleries.count() / RECOMMENDED_ROWS   

    if spare==3:
        galleries_thumbs_3 = reversed(galleries_thumbs[:3])
        galleries_thumbs = galleries_thumbs[3:number_rows*RECOMMENDED_ROWS+3]
    elif spare==2:
        galleries_thumbs_2 = reversed(galleries_thumbs[:2])
        galleries_thumbs = galleries_thumbs[2:number_rows*RECOMMENDED_ROWS+2]
    elif spare==1:
        galleries_thumbs_1 = reversed(galleries_thumbs[:1])
        galleries_thumbs = galleries_thumbs[1:number_rows*RECOMMENDED_ROWS+1]

    number_pictures_all = ((pictures_all.count()/RECOMMENDED_ROWS)*RECOMMENDED_ROWS)    
    if pictures_all:
        main_picture = pictures_all[0]
        twitter_gallery = pictures_all[0:4]
    else:
        main_picture = None
        if galleries:
            twitter_gallery = [ x.picture_set.first() for x in galleries[0:4] ]
            main_picture = twitter_gallery[0]
        else:
            twitter_gallery = None
            
    galleries_odd = False

    if galleries:
        if galleries.count() % 2 == 1:
            galleries_odd = True
    
    return render(request, 'user_gallery.html', {
        'pictures_all':pictures_all,
        'pictures_clearing':pictures_clearing,
        'pictures_all_3':pictures_all_3,
        'pictures_all_2':pictures_all_2,
        'pictures_all_1':pictures_all_1,
        'pictures_count':  pictures_count,
        'galleries_thumbs':galleries_thumbs,
        'galleries_thumbs_3':galleries_thumbs_3,
        'galleries_thumbs_2':galleries_thumbs_2,
        'galleries_thumbs_1':galleries_thumbs_1,        
        'twitter_gallery':twitter_gallery,
        'user_gravatar_url':user_gravatar_url,
        'picup_user':picup_user,
        'galleries':galleries,
        'gallery':gallery,
        'picup_profile':picup_profile,
        'main_picture':main_picture,
        'picture':main_picture,
        'galleries_odd':galleries_odd})

def karma(request):
    """Public karma ranking view.
    
    Note
    ----
    Deprecated.
    """
    karmas_all = PicupProfile.objects.all().order_by('-karma')[0:24]
    
    karma_profiles = karmas_all[0:3]
    karma_profiles_small = karmas_all[3:15] 

    return render(request, "karma.html",
        {'karma_profiles':karma_profiles,
        'karma_profiles_small':karma_profiles_small})

@login_required
def accounts_remove(request):
    """Remove an account view.
    
    Note
    ----
    Removing can happen in a two ways:
        * asynchronously with usage of the rabbit
        * synchronously as a fallback
    """
    
    if request.POST:
        user_id = request.user.id
        remove_dict = {"user_id":user_id}
        try:
            channel = get_rabbit_channel()
            channel.queue_declare(queue='picup_remove')
            channel.basic_publish(exchange='',routing_key='picup_remove',body=json.dumps(remove_dict))
        except:
            user = User.objects.filter(id=user_id)
            picup_profile = PicupProfile.objects.filter(user=user)
            pictures = Picture.objects.filter(user=user)
            galleries = Gallery.objects.filter(user=user)
            for picture in pictures:
                picture.picture.delete()
                picture.picture_thumb.delete()
                picture.picture_smart.delete()
                picture.picture_medium.delete()
                picture.delete()

            for gallery in galleries:
                gallery.delete()
            picup_profile.delete()
            user.delete()
        logout(request)
        
        return redirect('/')
    
    return render(request, "accounts_remove.html",{})

def tos(request):
    """Terms of service view.
    """
    return render(request, "tos.html",{})

def api(request):
    """Api description view.
    """
    return render(request, "api.html",)

def browse_json(request, users=None, galleries=None):
    """Browse JSON view.
    """
    galleries_dict = [ serialize_gallery(x) for x in galleries ]
    users_dict = [ serialize_user(x) for x in users]
    response_dict = {}
    response_dict['galleries'] = galleries_dict
    response_dict['users'] = users_dict
    return HttpResponse(json.dumps(response_dict), content_type="application/json")


def browse(request):
    """Browse view.
    """
    galleries,users = get_recommended()

    checkbox_licenses = []
    for license in CHOICES_LICENSE[2:]:
        new_license = [license[0], license[1].split(' ')[-1]]
        checkbox_licenses.append(new_license)

    response_dict = {}
    response_dict['galleries'] = galleries[0:24]
    response_dict['users'] = users[0:8]
    response_dict['checkbox_licenses'] = checkbox_licenses

    if request.GET.has_key('format'):
        if request.GET['format']=='json':
            return(browse_json(request, users, galleries))

    return render(request, "browse.html",response_dict)

def browse_galleries(request):
    """Browse galleries.
    """
    galleries,users = get_recommended_all()
    response_dict = {}
    response_dict['galleries'] = galleries
    if request.GET.has_key('format'):
        if request.GET['format']=='json':
            return(browse_json(request, [], galleries))
    return render(request, "browse_galleries.html",response_dict)

def browse_users(request):
    """Browse users.
    """
    galleries,users = get_recommended_all()
    response_dict = {}
    response_dict['users'] = users
    if request.GET.has_key('format'):
        if request.GET['format']=='json':
            return(browse_json(request, users, []))    
    return render(request, "browse_users.html",response_dict)

def _do_login(strategy, user):
    login(strategy.request, user)
    # user.social_user is the used UserSocialAuth instance defined in
    # authenticate process
    social_user = user.social_user
    if strategy.setting('SESSION_EXPIRATION', True):
        # Set session expiration date if present and not disabled
        # by setting. Use last social-auth instance for current
        # provider, users can associate several accounts with
        # a same provider.
        expiration = social_user.expiration_datetime()
        if expiration:
            try:
                strategy.request.session.set_expiry(
                    expiration.seconds + expiration.days * 86400
                )
            except OverflowError:
                # Handle django time zone overflow
                strategy.request.session.set_expiry(None)


class MyResponse(object):
    pass

@csrf_exempt
def mobile_persona(request, backend='persona', *args, **kwargs):
    """Mobile persona view.
    """
    @strategy('social:complete')
    def mobile_persona_int(request, backend='persona', *args, **kwargs):    
        assertion = request.POST['assertion']
        errors = []
        api_key  = None
        user_id = 0
        try:
            do_complete(request.social_strategy, _do_login, request.user,
                        redirect_name='', *args, **kwargs)
            picup_profile = get_or_create_profile(request.user)
            api_key = picup_profile.api_key
            user_id = picup_profile.user.id
        except Exception as e:
            import traceback
            traceback.print_exc()
            errors.append(['auth_failed'])
        response = requests.post('https://browserid.org/verify', 
            data={
            'assertion':assertion,
            'audience':'picup.it'
            })
        response_json = json.loads(response.text)
        response_json['errors'] = errors

        if api_key:
            response_json['api_key'] = api_key

        if user_id > 0:
            response_json['user_id'] = user_id


        response_json = json.dumps(response_json)
        my_response = MyResponse()
        my_response.text = response_json

        return my_response

    response = mobile_persona_int(request, backend)


    return HttpResponse(response.text, content_type="application/json")


@xframe_options_exempt
def mobile_auth(request):
    """Mobile auth view.
    """
    if request.user.is_authenticated():
        return redirect('/mobile/ffoslogged/')
    return render(request, "mobile_auth.html")

@xframe_options_exempt
@login_required
def mobile_data(request):
    """Mobile data view.
    """
    picup_profile = get_or_create_profile(request.user)
    data = {}
    data['email'] = request.user.email
    data['api_key'] =picup_profile.api_key
    return HttpResponse(json.dumps(data),content_type='application/json')

@xframe_options_exempt
def mobile_ffoslogged(request):
    """Mobile FirefoxOS logged view.
    """
    return render(request, "ffoslogged.html")

def signin(request):
    """Sign in view.
    """
    return render(request, "signin.html")

def error404(request):
    """Error 404 view.
    """
    return render(request, "404.html", status=404)

def picture_view_json(request, picture_id):
    """Single picture JSON view.
    
    Parameters
    ----------
    picture_id : int
    """
    return picture_view(request, picture_id,True)

def picture_view(request, picture_id,oembed=False):
    """Single picture view.
    
    Parameters
    ----------
    picture_id : int
    oembed : bool
    """
    try:
        picture = Picture.objects.get(id=picture_id)
    except Picture.DoesNotExist:
        raise Http404

    user_gravatar_url = get_gravatar_url(picture.user.email)
    picup_profile = get_or_create_profile(picture.user)
    gallery = None

    picture_next = picture_previous = picture_first = picture_last = None

    # To show the background below top bar
    if not picup_profile.profile_picture:
        galleries = Gallery.objects.filter(user=picture.user).order_by('title').annotate(num_pictures=Count('picture')).filter(num_pictures__gt=0)[0:1]
    else:
        galleries = None
    gallery_pictures = []
    metadata_dict = {}
    if picture.gallery:
        if picture.gallery.exif:
            metadata = get_metadata(picture.picture.file.name)
            metadata_dict = {}
            for mkey in metadata.exif_keys:
                try:
                    if mkey.find('Thumbnail')<0:
                        if len(metadata[mkey].value.__str__()) < 32:
                            new_mkey = mkey.replace('Exif.','')
                            metadata_dict[new_mkey] = metadata[mkey].value
                except UnicodeEncodeError:
                    pass
                except ValueError:
                    pass
            metadata_dict = collections.OrderedDict(sorted(metadata_dict.items()))


        gallery = picture.gallery
        gallery_pictures = gallery.picture_set.all()
        pictures_ids = [ x.id for x in gallery_pictures]
        picture_pos = pictures_ids.index(int(picture_id))
        #TODO: Optimize
        picture_first = Picture.objects.get(id=pictures_ids[0])
        picture_last = Picture.objects.get(id=pictures_ids[len(pictures_ids)-1])
        if picture_pos<len(pictures_ids)-1:
            picture_next = Picture.objects.get(id=pictures_ids[picture_pos+1])
        if picture_pos>0:
            picture_previous = Picture.objects.get(id=pictures_ids[picture_pos-1])

    others_pictures = []

    if picture.gallery:
        others_pictures = Picture.objects.filter(user=picture.user, gallery=picture.gallery).exclude(id=picture.id)
        if picture_next:
            others_pictures = others_pictures.exclude(id = picture_next.id)
        if picture_previous:
            others_pictures = others_pictures.exclude(id = picture_previous.id)
        others_pictures = others_pictures[0:4]

    metadata_dict_legacy = metadata_dict
    metadata_dict = {}
    for meta_entity in metadata_dict_legacy.keys():
        try:
            metadata_dict[meta_entity] = metadata_dict_legacy[meta_entity]
        except UnicodeDecodeError:
            pass
        except UnicodeEncodeError:
            pass

    if oembed==False:
        return render(request, "picture_view.html", {
        'picture':picture,
        'picup_profile':picup_profile,
        'picture_next':picture_next,
        'picture_first':picture_first,
        'picture_last':picture_last,
        'picture_previous':picture_previous,
        'galleries':galleries,
        'metadata':metadata_dict,
        'user_gravatar_url':user_gravatar_url,
        'gallery_pictures': gallery_pictures,
        'others_pictures':others_pictures})
    else:
        result = {}
        result['version'] = "1.0"
        result['type'] = 'photo'
        result['title'] = 'PicUp - Pictures Sharing'
        result['url'] = 'https://picup.it/p/%s/' % picture_id
        result['author_name'] = 'PicUp user'
        result['provider_name'] = 'PicUp'
        result['provider_url'] = 'https://picup.it/'
        result["width"] = "516"
        result["height"]  ="320"
        result["html"] = "<iframe src='https://picup.it/p/%s/' width='516px' height='315px' frameBorder='0'></iframe>" % picture_id
        return HttpResponse(json.dumps(result),content_type='application/json')

def index(request):
    """Home page view.
    """
    galleries,users = get_recommended()

    if galleries.count()>3:
        cut = randint(0,galleries.count()-3)
        galleries = galleries[0:4]
    if users.count()>3:
        cut = randint(0,users.count()-3)
        users = users[cut:2+cut]
    pictures_own = None
    try:
        pictures = Picture.objects.all().order_by("-id")[0:48]
    except IndexError:
        pictures = None

    if request.user.is_authenticated():
        pictures_own = Picture.objects.filter(user=request.user).order_by("-id")[:16]
        
    picture_feat = None
    if pictures:
        picture_feat = pictures[0]

    all_pictures = Picture.objects.all().count()
    all_users = User.objects.all().count()
    all_galleries = Gallery.objects.all().count()
    banners = PictureDescription.banners_objects.all()[0:32]

    return render(request, "homepage.html", {
        'pictures':pictures, 
        'pictures_own':pictures_own,
        'users':users,
        'galleries':galleries,
        'all_pictures': all_pictures,
        'all_galleries': all_galleries,
        'all_users': all_users,
        'picture_feat':picture_feat,
        'banners':banners})


@login_required
def upload_picture(request):
    """Upload picture view.
    """
    if request.method == 'POST':
        picture = Picture()
        picture.user = request.user
        form = UploadFileForm(request.POST, request.FILES, instance=picture)
        response = {}

        if form.is_valid():
            picture.picture = request.FILES['picture']
            picture.picture.name = unidecode(picture.picture.name)
            picture.save()

            ### nasty error at 3:45 AM ;/
            try:
                rotate_picture(picture)           
                picture.update_thumb()
                picture.save()
            except:
                import sys, traceback
                traceback.print_exc(file=sys.stdout)
                picture.delete()
                response['status'] = 'UPLOAD ERROR. PUT HELMET ON AND EVACUATE!!!'
                response = json.dumps(response)
                return HttpResponse(response)
            response['url'] = picture.picture_thumb.url
            response['id'] = picture.id
            response = json.dumps(response)
        else:
            response = "Failed to upload"
    else:
        if request.GET.has_key('gallery_id'):
            preffered_gallery=int(request.GET['gallery_id'])
        else:
            preffered_gallery=None
        galleries =  Gallery.objects.filter(user=request.user)
        return render(request, "upload.html", 
            {'galleries':galleries,'preffered_gallery':preffered_gallery})
    return HttpResponse(response)
