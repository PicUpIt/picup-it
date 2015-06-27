from django.contrib.syndication.views import Feed
from django.contrib.syndication.views import FeedDoesNotExist
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User  

from models import Gallery, Picture

class UserFeed(Feed):
    def get_object(self, request, user_id):
        return get_object_or_404(User, pk=user_id)

    def title(self, obj):
        return "%s RSS feed from PicUp.It" % obj.username

    def link(self, obj):
        return '/u/%s/' % obj.id

    def item_description(self, item):
        return '%s' % item.description

    def item_title(self, item):
        return '%s' % item.title

    def description(self, obj):
        return "%s's galleries" % obj.username

    def items(self, obj):
        return Gallery.objects.filter(user=obj).order_by('title').annotate(num_pictures=Count('picture')).exclude(license__in=[0,1]).filter(num_pictures__gt=1).order_by('-id')[:30]

class GalleryFeed(Feed):
    description_template = 'feeds/gallery_description.html'

    def get_object(self, request, user_id, gallery_id):
        return get_object_or_404(Gallery, pk=gallery_id)

    def title(self, obj):
        return "%s by %s" % (obj.title,obj.user.username)

    def link(self, obj):
        return obj.get_absolute_url()

    def item_title(self,item):
        return "width: %s height: %s on %s" % (item.width, item.height, item.created)

    def description(self, obj):
        return "%s" % (obj.description)

    def items(self, obj):
        return Picture.objects.filter(gallery=obj).order_by('-id')[:30]        