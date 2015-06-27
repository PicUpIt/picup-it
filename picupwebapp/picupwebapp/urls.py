from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from picupwebapp.picture.feed_views import UserFeed, GalleryFeed

urlpatterns = patterns('',
    url(r'^\.well-known/webfinger$', 'picupwebapp.picture.webfinger_views.main', name='webfinger'),
    url(r'^\.well-known/host-meta$', 'picupwebapp.picture.webfinger_views.host_meta', name='host_meta'),
    url(r'^api/statuses/user_timeline/(?P<user_id>\d*).atom$', 'picupwebapp.picture.webfinger_views.user_timeline', name='user_timeline'),
    url(r'^main/push/hub$', 'picupwebapp.picture.webfinger_views.push_hub', name='push_hub'),

    url(r'^login/openid_pre/$', 'picupwebapp.picture.views.openid_pre', name='openid_pre'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^p/(?P<picture_id>\d*)/$', 'picupwebapp.picture.views.picture_view', name='picture_view'),    
    url(r'^p/(?P<picture_id>\d*)\.json$', 'picupwebapp.picture.views.picture_view_json', name='picture_view_oembed'),
	url(r'^picup$', 'picupwebapp.picture.views.upload_picture', name='upload'),
	url(r'^$', 'picupwebapp.picture.views.index', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += patterns('',
    url(r'^int_call/description/(?P<picture_id>\d*)/$', 'picupwebapp.picture.int_calls.description', name='intcall_description'),
    url(r'^int_call/picture/(?P<picture_id>\d*)/$', 'picupwebapp.picture.int_calls.picture', name='intcall_picture'),
    url(r'^int_call/profile/$', 'picupwebapp.picture.int_calls.profile', name='intcall_profile'),
    url(r'^int_call/gallery/$', 'picupwebapp.picture.int_calls.gallery', name='intcall_gallery'),
    url(r'^int_call/simply_browse/$', 'picupwebapp.picture.int_calls.simply_browse', name='simply_browse'),
)
# views for the API
urlpatterns += patterns('',
    url(r'^api/browse/$', 'picupwebapp.picture.api_views.api_browse', name='api_browse'),
    url(r'^api/browse/galleries/$', 'picupwebapp.picture.api_views.api_browse_galleries', name='api_browse_galleries'),
    url(r'^api/browse/users/$', 'picupwebapp.picture.api_views.api_browse_users', name='api_browse_users'),
    url(r'^api/auth/$', 'picupwebapp.picture.api_views.auth', name='api_auth'),
    url(r'^api/upload/$', 'picupwebapp.picture.api_views.api_upload', name='api_upload'),
    url(r'^api/gallery/(?P<gallery_id>\d*)/$', 'picupwebapp.picture.api_views.api_gallery', name='api_gallery'),
    url(r'^api/user/(?P<user_id>\d*)/$', 'picupwebapp.picture.api_views.api_user', name='api_user'),
    url(r'^api/picture/(?P<picture_id>\d*)/$', 'picupwebapp.picture.api_views.api_picture', name='api_picture'),
    )

urlpatterns += patterns('',
    url(r'^mobile/auth/$', 'picupwebapp.picture.views.mobile_auth', name='mobile_auth'),
    url(r'^mobile/data/$', 'picupwebapp.picture.views.mobile_data', name='mobile_data'),
    url(r'^mobile/persona/$', 'picupwebapp.picture.views.mobile_persona', name='mobile_persona'),
    url(r'^mobile/ffoslogged/$', 'picupwebapp.picture.views.mobile_ffoslogged', name='mobile_ffoslogged'),
    url(r'^accounts/profile/$','picupwebapp.picture.views.accounts_profile', name='accounts_profile'),
    url(r'^accounts/remove/$','picupwebapp.picture.views.accounts_remove', name='accounts_remove'),
    
    url(r'^signin/$','picupwebapp.picture.views.signin', name='signin'),
    url(r'^deerbox/$','picupwebapp.picture.views.accounts_profile', name='deerbox'),
    url(r'^deerbox/gallery/(?P<gallery_id>\d*)/$','picupwebapp.picture.views.deerbox_gallery', name='deerbox_gallery'),
    url(r'^u/(?P<user_id>\d*)/$','picupwebapp.picture.views.user_gallery', name='user_galleries'),
    url(r'^u/(?P<user_id>\d*)/rss/$', UserFeed()),
    url(r'^u/(?P<user_id>\d*)/(?P<gallery_id>\d*)/$','picupwebapp.picture.views.user_gallery', name='user_gallery'),
    url(r'^u/(?P<user_id>\d*)/(?P<gallery_id>\d*)/rss/$',GalleryFeed()),
    url(r'^browse/$','picupwebapp.picture.views.browse', name='browse'),
    url(r'^browse/users/$','picupwebapp.picture.views.browse_users', name='browse_users'),
    url(r'^browse/galleries/$','picupwebapp.picture.views.browse_galleries', name='browse_galleries'),
    url(r'^karma/$','picupwebapp.picture.views.karma', name='karma'),
    url(r'^tos/$','picupwebapp.picture.views.tos', name='tos'),
    url(r'^api/$','picupwebapp.picture.views.api', name='api'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'})
)

