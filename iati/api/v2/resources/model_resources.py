from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.models import create_api_key
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from data.models.organisation import Organisation, RecipientCountryBudget, RecipientOrgBudget, TotalBudget, Activity, Transaction, PolicyMarker


class OrganisationResource(ModelResource):
    class Meta:
        queryset = Organisation.objects.all()
        resource_name = 'organisations'
        serializer = Serializer(formats=['xml', 'json', 'yaml'])

class ActivityResource(ModelResource):
    class Meta:
        queryset = Activity.objects.all()
        resource_name = 'activities'
        serializer = Serializer(formats=['xml', 'json', 'yaml'])
        filtering = {
            # example to allow field specific filtering.
            'activity_status': ALL,
            }