from api.handlers import resource_registrar
from data.models import Organisation, RecipientCountryBudget, RecipientOrgBudget, TotalBudget, Activity, Transaction, PolicyMarker
from django.conf.urls.defaults import *
from piston.doc import documentation_view

resource_registrar.register(Transaction, Activity, TotalBudget, RecipientOrgBudget,
    RecipientCountryBudget, Organisation, PolicyMarker)

urlpatterns = patterns('api.views',
    url('^data/last_updated/$', 'last_updated'),
    url('^(?P<app_label>\w+)/(?P<model_name>\w+)/$', 'api', name='index'),
    url('^(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<id>\w+)/$', 'api', name='object'),
    url('^documentation/$', documentation_view, name='documentation'),
)