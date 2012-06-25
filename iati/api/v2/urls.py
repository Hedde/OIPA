# Django specific
from django.conf.urls import *

# Tastypie specific
from tastypie.api import Api

# App specific
from api.v2.resources.model_resources import OrganisationResource
from api.v2.resources.model_resources import ActivityResource


v2_api = Api(api_name='v2')
v2_api.register(OrganisationResource())
v2_api.register(ActivityResource())

urlpatterns = patterns('',
    (r'^$', 'api.v2.views.docs_index'),
    (r'^v2/$', 'api.v2.views.docs_index'),
    (r'', include(v2_api.urls)),
)