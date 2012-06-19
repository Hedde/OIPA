# Tastypie specific
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.models import create_api_key
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.constants import ALL, ALL_WITH_RELATIONS

# Data specific
from data.models.activity import IATIActivity
from data.models.organisation import Organisation


class OrganisationResource(ModelResource):
    class Meta:
        queryset = Organisation.objects.all()
        resource_name = 'organisations'
        serializer = Serializer(formats=['xml', 'json', 'yaml'])
        filtering = {
            # example to allow field specific filtering.
            'org_name': ALL,
        }

    def dehydrate(self, bundle):
        bundle.data['type'] = self.obj_get(ref=bundle.data['ref']).get_type_display()
        return super(OrganisationResource, self).dehydrate(bundle)


class ActivityResource(ModelResource):
    reporting_organisation = fields.ForeignKey('api.v2.resources.OrganisationResource', attribute='ref', full=True, null=True)

    class Meta:
        queryset = IATIActivity.objects.all()
        resource_name = 'activities'
        serializer = Serializer(formats=['xml', 'json', 'yaml'])
        filtering = {
            # example to allow field specific filtering.
            'activity_status': ALL,
            'recipient_country_code': ALL
            }

    def dehydrate(self, bundle):
        bundle.data['reporting_organisation'] = self.obj_get(iati_identifier=bundle.data['iati_identifier']).reporting_organisation.org_name
        return bundle
