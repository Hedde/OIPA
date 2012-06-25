# Django specific
from django.conf.urls import *
from django.http import HttpResponseRedirect

# Tastypie specific
from tastypie.api import Api

# App specific
from api.v2.resources.model_resources import OrganisationResource
from api.v2.resources.model_resources import ActivityResource


v2_api = Api(api_name='v2')
v2_api.register(OrganisationResource())
v2_api.register(ActivityResource())

def redirect(request):
    return HttpResponseRedirect('/api/v2/docs/')

urlpatterns = patterns('',
    (r'^$', redirect),
    (r'^v2/$', redirect),
    (r'^v2/docs/$', 'api.v2.views.docs_index'),
    (r'^v2/docs/resources/$', 'api.v2.views.docs_resources'),
    (r'^v2/docs/filtering/$', 'api.v2.views.docs_filtering'),
    (r'^v2/docs/license/$', 'api.v2.views.docs_license'),
    (r'', include(v2_api.urls)),
)