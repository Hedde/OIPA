# Django specific
from django.conf.urls import *


urlpatterns = patterns('',
    url('^v1/', include('api.v1.urls', 'api')),
    url('', include('api.v2.urls')),
)