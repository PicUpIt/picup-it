"""Purely experiment code here.

Maybe someone would like to rewrite it correctly.
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User

from models import Picture
from django.views.decorators.csrf import csrf_exempt
import json
def main(request):
    if request.GET.has_key('resource'):
        resource = request.GET['resource']
        if resource == 'https://picup.it/':
            return render(request, "webfinger/host_meta.json",
                          content_type="application/json")
        elif resource.startswith("acct"):
            useruri = resource.split(':')[1]
            userid = int(useruri.split('@')[0])
            if userid == 1:
                return HttpResponse('')
            return render(request, "webfinger/resource_reply.json", {'userid':userid})
    return HttpResponse('no')


def host_meta(request):
    return render(request, "webfinger/host_meta.json",
                  content_type="application/json")

from django.utils.html import escape

def user_timeline(request, user_id):

    d = {}

    if user_id!=1:
        user = User.objects.get(id=user_id)
        pictures = Picture.objects.filter(user=user).exclude(gallery__license__in=[0,1])[0:10]
        d['pictures'] = pictures
        d['user'] = user
        d['userid'] = user_id

        for picture in pictures:
            picture.statusnet_text = escape('<a href="https://picup.it/p/%s" title="https://picup.it/p/%s">https://picup.it/p/%s/ %s</a>' % (picture.id, picture.id, picture.id, picture.description))

        return render(request, "webfinger/timeline.atom",	d,
                      content_type="application/atom+xml",)
@csrf_exempt
def push_hub(request):
    if request.POST:
        print "PUSH_HUB",request.POST
        return HttpResponse(json.dumps(request.POST), status=202)
    else:
        print "PUSH_HUB",request.POST
        return HttpResponse(json.dumps(request.GET))