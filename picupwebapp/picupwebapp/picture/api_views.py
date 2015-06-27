"""Views for the API.

authentication schema:
username: email@example.com
password: api_key
"""
from functools import wraps
import json
from unidecode import unidecode
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User
from django.utils.decorators import decorator_from_middleware, available_attrs
from models import PictureDescription, Gallery
from views import upload_picture, browse_json, get_recommended_all, get_recommended
from views import serialize_gallery, serialize_user, serialize_picture
from picupwebapp.picprofile.models import PicupProfile

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401
    
content_401 = json.dumps({'error':'401'})
content_credentials = json.dumps({'error':'bad credentials'})
content_200 = json.dumps({'status':'OK'})

def api_gallery(request, gallery_id):
    gallery = Gallery.objects.get(id=gallery_id)
    gallery_json = serialize_gallery(gallery, True)
    return HttpResponse(json.dumps(gallery_json), content_type="application/json")

def api_user(request, user_id):
    user = User.objects.get(id=user_id)
    user_json = serialize_user(user, True)
    return HttpResponse(json.dumps(user_json), content_type="application/json")

def api_picture(request, picture_id):
    picture = Picture.objects.get(id=picture_id)
    picture_json = serialize_picture(picture)
    return HttpResponse(json.dumps(picture_json), content_type="application/json")

def api_browse(request):
    galleries,users = get_recommended()
    return(browse_json(request, users, galleries))

def api_browse_galleries(request):
    galleries,users = get_recommended_all()
    return(browse_json(request, [], galleries))

def api_browse_users(request):
    galleries,users = get_recommended_all()
    return(browse_json(request, users, []))

def require_api_login(view):
    def _wrapped_view(request, *args, **kwargs):
        if request.POST:
            if not request.POST.has_key('email') or not request.POST.has_key('api_key'):
                return HttpResponseUnauthorized(content_401)
        else:
            if not request.GET.has_key('email') or not request.GET.has_key('api_key'):
                return HttpResponseUnauthorized(content_401)
        try:
            user = User.objects.get(email=request.POST['email'])
            api_key = request.POST['api_key']
            picup_profile = PicupProfile.objects.filter(user=user).get(api_key=api_key)
        except PicupProfile.DoesNotExist:
            return HttpResponse(content_credentials)
        except User.DoesNotExist:
            return HttpResponse(content_credentials)
        return view(request, *args, **kwargs)
    return _wrapped_view


@csrf_exempt
@require_api_login
def auth(request):
    return HttpResponse(content_200)

from models import Picture
from forms import UploadFileForm
from tools import rotate_picture


@csrf_exempt
@require_api_login
def api_upload(request):
    if request.method == 'POST':
        picture = Picture()
        user = User.objects.get(email=request.POST['email'])
        picture.user = user
        form = UploadFileForm(request.POST, request.FILES, instance=picture)
        if form.is_valid():
            picture.picture = request.FILES['picture']
            if request.POST.has_key('gallery_id'):
                gallery = Gallery.objects.get(id=request.POST['gallery_id'], user=user)
                picture.gallery = gallery

            picture.picture.name = unidecode(picture.picture.name)
            picture.save()
            rotate_picture(picture)
            picture.update_thumb()

            if request.POST.has_key('description'):
                picture_description = PictureDescription(picture=picture)
                picture_description.text = request.POST['description']
                picture_description.save()  

            response = {'status':'OK'}
            response['data'] = serialize_picture(picture)
            return HttpResponse(json.dumps(response))

    return HttpResponse(content_200)
