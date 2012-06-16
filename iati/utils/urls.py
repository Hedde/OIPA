from django.conf.urls import *


urlpatterns = patterns('utils.views',
    url('add_activity_file/', 'upload_activity_set'),
)