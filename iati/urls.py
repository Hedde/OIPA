from django.conf.urls import *
from django.contrib import admin
from django.conf import settings


admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^api/', include('api.urls')),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
