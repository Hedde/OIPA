from urllib2 import HTTPRedirectHandler
from api.v1.handlers import resource_registrar
#from data.models.organisation import Organisation, RecipientCountryBudget, RecipientOrgBudget, TotalBudget, Activity, Transaction, PolicyMarker
from django.conf.urls import *
from piston.doc import documentation_view

#resource_registrar.register(Transaction, Activity, TotalBudget, RecipientOrgBudget,
#    RecipientCountryBudget, Organisation, PolicyMarker)

urlpatterns = patterns('api.v1.views',
    url('^$', documentation_view),
    url('^data/last_updated/$', 'last_updated'),
    url('^(?P<app_label>\w+)/(?P<model_name>\w+)/$', 'api', name='index'),
    url('^(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<id>\w+)/$', 'api', name='object'),
    url('^documentation/$', documentation_view, name='documentation'),
)