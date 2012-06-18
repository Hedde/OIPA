from django.conf.urls import *

from tastypie.api import Api

from api.v2.resources.model_resources import OrganisationResource
#from api.v2.resources.model_resources import ActivityResource
#from api.v2.resources.model_resources import SectorResource

v2_api = Api(api_name='v2')
v2_api.register(OrganisationResource())
#v2_api.register(ActivityResource())
#v2_api.register(SectorResource())

urlpatterns = patterns('',
    (r'^$', 'api.v2.views.docs'),
    (r'^v2/$', 'api.v2.views.docs'),
    (r'', include(v2_api.urls)),
)