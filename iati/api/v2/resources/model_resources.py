# Django specific
from django.db.models import Q

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
from data.models.activity import IATIActivityCountry
from data.models.activity import IATIActivityTitle
from data.models.common import Country
from data.models.organisation import Organisation


class OrganisationResource(ModelResource):
    class Meta:
        queryset = Organisation.objects.all()
        resource_name = 'organisations'
        serializer = Serializer(formats=['xml', 'json'])
        filtering = {
            # example to allow field specific filtering.
            'org_name': ALL,
            'ref': ALL,
        }

    def dehydrate(self, bundle):
        obj = self.obj_get(ref=bundle.data['ref'])
        bundle.data['type'] = obj.get_type_display()
#        bundle.data['total_activities'] = obj.iatiactivity_set.count()
        return super(OrganisationResource, self).dehydrate(bundle)


class ActivityResource(ModelResource):
    """
    @description
    Displays Activities, with nested Organisation

    @implementation
    http://127.0.0.1:8080/api/v2/activities/?format=json&query=EMTA
    http://127.0.0.1:8080/api/v2/activities/?format=json
    http://127.0.0.1:8080/api/v2/activities/?format=json&reporting_organisation__ref=SE-6
    http://127.0.0.1:8080/api/v2/activities/?format=json&reporting_organisation__org_name__icontains=Oxfam
    """
    reporting_organisation = fields.ForeignKey(OrganisationResource, attribute='reporting_organisation', full=True, null=True)

    class Meta:
        queryset = IATIActivity.objects.all()
        resource_name = 'activities'
        serializer = Serializer(formats=['xml', 'json'])
        filtering = {
            # example to allow field specific filtering.
            'activity_status': ALL,
            'iati_identifier': ALL,
            'reporting_organisation': ALL_WITH_RELATIONS
        }

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(ActivityResource, self).apply_filters(request,
            applicable_filters)
        query = request.GET.get('query', None)
        countries = request.GET.get('countries', None)
        filters = {}
        if countries:
            # @todo: implement smart filtering with seperator detection
            countries = countries.replace('|', ' ').replace('-', ' ').split(' ')
            filters.update(dict(iatiactivitycountry__country__iso__in=countries))
        if query:
            qset = (
                Q(iatiactivitytitle__title__icontains=query, **filters) |
                Q(iatiactivitydescription__description__icontains=query, **filters)
            )
            base_object_list = base_object_list.filter(qset).distinct()
        return base_object_list.filter(**filters).distinct()

    def dehydrate(self, bundle):
        obj = self.obj_get(iati_identifier=bundle.data['iati_identifier'])
        titles = {}
        for title in obj.iatiactivitytitle_set.all():
            titles[title.language.code] = title.title
        bundle.data['title'] = titles
        descriptions = {}
        for description in obj.iatiactivitydescription_set.all():
            descriptions[description.language.code] = description.description
        bundle.data['description'] = descriptions
        return bundle
