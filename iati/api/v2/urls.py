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

def api_v2_docs(request):
    return HttpResponseRedirect('/api/v2/docs/')

urlpatterns = patterns('',
    (r'^$', api_v2_docs),
    (r'^v2/$', api_v2_docs),
    url(r'^v2/docs/$', 'api.v2.views.docs_index', name='docs'),
    url(r'^v2/docs/getting-started/$', 'api.v2.views.docs_start', name='start_docs'),
    url(r'^v2/docs/resources/$', 'api.v2.views.docs_resources', name='resource_docs'),
    url(r'^v2/docs/filtering/$', 'api.v2.views.docs_filtering', name='filter_docs'),
    (r'', include(v2_api.urls)),
)