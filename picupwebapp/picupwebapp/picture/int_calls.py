import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from models import Picture, Gallery, PictureDescription, create_gallery, get_user_galleries, gallery_insert_picture
from picupwebapp.picprofile.models import  PicupProfile
from django.db.models import Count
from django.conf import settings
from django.shortcuts import render, redirect
from tools_views import get_recommended_filter

@csrf_exempt
@login_required
def gallery(request):
    if request.POST:
        if request.POST.has_key('create'):
            title = request.POST['gallery_title']
            gallery = create_gallery(title, "", request.user)
            response = gallery.get_json()
            return HttpResponse(response)
        
        if request.POST.has_key('edit'):
            gallery_id = request.POST['gallery_id']
            gallery = Gallery.objects.get(id=gallery_id, user=request.user)

            try:
                title = request.POST['title']
                gallery.title = title
            except KeyError:
                pass

            try:
                license = request.POST['license']
                gallery.license = license
            except KeyError:
                pass

            try:
                description = request.POST['description']
                gallery.description = description
            except KeyError:
                pass

            try:
                exif = request.POST['exif']
                if exif=='true':
                    gallery.exif = True
                else:
                    gallery.exif = False
            except KeyError:
                pass
            
            gallery.save()
            return HttpResponse(json.dumps({'result':'OK', 
                'title':gallery.title, 'description':gallery.description, 'exif':gallery.exif}))

        if request.POST.has_key('insert_picture'):
            gallery_id = request.POST['gallery_id']
            picture_id = request.POST['picture_id']
            gallery = Gallery.objects.get(id=gallery_id, user=request.user)
            picture = Picture.objects.get(id=picture_id, user=request.user)
            gallery_insert_picture(gallery, picture)
            return HttpResponse(json.dumps({'result':'ok'}))
        if request.POST.has_key('remove'):
            gallery_id = request.POST['gallery_id']
            gallery = Gallery.objects.get(id=gallery_id, user=request.user)
            pictures = Picture.objects.filter(gallery_id=gallery_id, user=request.user)
            for picture in pictures:
                picture.gallery = None
                picture.save()
            gallery.delete()
            return HttpResponse(json.dumps({'result':'ok'}))
            pass
        if request.POST.has_key('remove_picture'):
            pass

@csrf_exempt
@login_required
def profile(request):
    if request.POST:
        if request.POST.has_key('username'):
            username = request.POST['username'].lower()

            if username in ['admin']:
                return HttpResponse('reseverd')            

            duplicate = User.objects.filter(username=username).exclude(id=request.user.id).count()
            if duplicate>0:
                return HttpResponse('duplicate')            
            request.user.username = username
            request.user.save()

            return HttpResponse('OK')
    return HttpResponse('NOOK')

@csrf_exempt
@login_required
def picture(request, picture_id):
    if request.POST:
        if request.POST.has_key('remove') and request.POST['remove']=='true':
            picture = Picture.objects.filter(user=request.user).get(id=picture_id)
            picture.delete()
            return HttpResponse('OK')
        if request.POST['set_banner']=='true':
            picture = Picture.objects.filter(user=request.user).get(id=picture_id)
            picup_profile = PicupProfile.objects.get(user=request.user)
            picup_profile.profile_picture = picture
            picup_profile.save()
            result = {}
            result['url'] = picture.picture_medium.url
            result['result'] = 'OK'
            return HttpResponse(json.dumps(result))
    return HttpResponse('NOOK')

@csrf_exempt
@login_required
def description(request, picture_id):
    if request.POST:
        picture = Picture.objects.filter(user=request.user).get(id=picture_id)
        key = 'picture_description'
        text = request.POST[key]
        picture_description, created = PictureDescription.objects.get_or_create(picture=picture)
        picture_description.text = text
        picture_description.save()
        return HttpResponse('OK')
    else:
        try:
            return HttpResponse(Picture.objects.get(id=picture_id).description.first().text)
        except AttributeError:
            return HttpResponse('')

def simply_browse(request):
    licenses_ids = [ int(x) for x in request.GET.getlist('licenses[]', '') ]
    galleries, users = get_recommended_filter(filter_list=licenses_ids)
    return render(request, "inc_thumbsbox.html", {'galleries':galleries})