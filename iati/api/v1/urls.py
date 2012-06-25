from django.conf.urls import *
from piston.doc import documentation_view

urlpatterns = patterns('api.v1.views',
    url('^$', documentation_view),
)