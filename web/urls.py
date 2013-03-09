
from django.conf.urls import patterns, include, url
from views import signup,login, post_handler, dashboard

urlpatterns = patterns('',
                       url('^signup/$',signup),
                       url('^login/$',login),
                       url('^(?P<user>\w[\w/-]*)/dashboard/$',dashboard),
                       url('^(?P<user>\w[\w/-]*)/dashboard/add_post/$',post_handler),
                       url('^(?P<user>\w[\w/-]*)/dashboard/(?P<post_id>\w[\w/-]*)/edit/$',post_handler),
                       )