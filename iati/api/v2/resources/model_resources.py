# Django specific
from django.db.models import Q

# Tastypie specific
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.constants import ALL, ALL_WITH_RELATIONS

# Data specific
from data.models.activity import IATIActivity
from data.models.organisation import Organisation

# App specific
from api.v2.resources.sub_model_resources import RecipientCountryResource
from api.v2.resources.sub_model_resources import RecipientRegionResource
from api.v2.resources.sub_model_resources import StatusResource
from api.v2.resources.sub_model_resources import SectorResource
from api.v2.resources.sub_model_resources import CollaborationTypeResource
from api.v2.resources.sub_model_resources import FlowTypeResource
from api.v2.resources.sub_model_resources import FinanceTypeResource
from api.v2.resources.sub_model_resources import AidTypeResource
from api.v2.resources.sub_model_resources import TiedAidStatusTypeResource
from api.v2.resources.sub_model_resources import ActivityBudgetResource
from api.v2.resources.sub_model_resources import TransactionResource


class OrganisationResource(ModelResource):
    """
    Resource for IATI Organisations
    """
    class Meta:
        queryset = Organisation.objects.all()
        resource_name = 'organisations'
        serializer = Serializer(formats=['xml', 'json'])
        excludes = ['date_created']
        filtering = {
            # example to allow field specific filtering.
            'org_name': ALL,
            'ref': ALL,
        }

    def dehydrate(self, bundle):
        obj = self.obj_get(ref=bundle.data['ref'])
        bundle.data['type'] = obj.get_type_display()
        bundle.data['total_activities'] = obj.iatiactivity_set.count()
        return super(OrganisationResource, self).dehydrate(bundle)


class ActivityResource(ModelResource):
    """
    Resource for IATI Activities
    """
    reporting_organisation = fields.ForeignKey(OrganisationResource, attribute='reporting_organisation', full=True, null=True)
    activity_status = fields.ForeignKey(StatusResource, attribute='activity_status', full=True, null=True)
    recipient_country = fields.ToManyField(RecipientCountryResource, 'iatiactivitycountry_set', full=True, null=True)
    recipient_region = fields.ToManyField(RecipientRegionResource, 'iatiactivityregion_set', full=True, null=True)
    sector = fields.ToManyField(SectorResource, 'iatiactivitysector_set', full=True, null=True)
    collaboration_type = fields.ForeignKey(CollaborationTypeResource, attribute='collaboration_type', full=True, null=True)
    default_flow_type = fields.ForeignKey(FlowTypeResource, attribute='default_flow_type', full=True, null=True)
    default_finance_type = fields.ForeignKey(FinanceTypeResource, attribute='default_finance_type', full=True, null=True)
    default_aid_type = fields.ForeignKey(AidTypeResource, attribute='default_aid_type', full=True, null=True)
    default_tied_status_type = fields.ForeignKey(TiedAidStatusTypeResource, attribute='default_tied_status_type', full=True, null=True)
    activity_budgets = fields.ToManyField(ActivityBudgetResource, 'iatiactivitybudget_set', full=True, null=True)
    activity_transactions = fields.ToManyField(TransactionResource, 'iatitransaction_set', full=True, null=True)

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
        # titles
        titles = {}
        for title in obj.iatiactivitytitle_set.all():
            titles[title.language.code] = title.title
        bundle.data['title'] = titles
        # descriptions
        descriptions = {}
        for description in obj.iatiactivitydescription_set.all():
            descriptions[description.language.code] = description.description
        bundle.data['description'] = descriptions
        return bundle
