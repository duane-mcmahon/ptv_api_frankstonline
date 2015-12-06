from django.conf.urls import *

urlpatterns = patterns('melbourne.views',
    url(r'^$', 'index', name='index'),
)
