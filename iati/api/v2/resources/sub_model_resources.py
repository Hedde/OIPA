# Tastypie specific
from tastypie.resources import ModelResource

# Data specific
from data.models.activity import IATIActivityCountry
from data.models.activity import IATIActivityRegion
from data.models.activity import IATIActivitySector
from data.models.common import ActivityStatusType
from data.models.common import CollaborationType
from data.models.common import FlowType
from data.models.common import AidType
from data.models.common import FinanceType
from data.models.common import TiedAidStatusType


class StatusResource(ModelResource):
    class Meta:
        queryset = ActivityStatusType.objects.all()
        fields = ['code']
        include_resource_uri = False

    def dehydrate(self, bundle):
        obj = self.obj_get(code=bundle.data['code'])
        bundle.data['name'] = obj.get_code_display()
        return bundle


class RecipientCountryResource(ModelResource):
    class Meta:
        queryset = IATIActivityCountry.objects.all()
        include_resource_uri = False

    def dehydrate(self, bundle):
        obj = self.obj_get(id=bundle.data['id'])
        bundle.data['iso'] = obj.country.iso
        bundle.data['name'] = obj.country.get_iso_display()
        bundle.data.pop('id')
        return bundle


class RecipientRegionResource(ModelResource):
    class Meta:
        queryset = IATIActivityRegion.objects.all()
        include_resource_uri = False

    def dehydrate(self, bundle):
        obj = self.obj_get(id=bundle.data['id'])
        bundle.data['code'] = obj.region.code
        bundle.data['name'] = obj.region.get_code_display()
        bundle.data.pop('id')
        return bundle


class SectorResource(ModelResource):
    class Meta:
        queryset = IATIActivitySector.objects.all()
        fields = ['code']
        include_resource_uri = False


class CollaborationTypeResource(ModelResource):
    class Meta:
        queryset = CollaborationType.objects.all()
        include_resource_uri = False


class FlowTypeResource(ModelResource):
    class Meta:
        queryset = FlowType.objects.all()
        include_resource_uri = False

    def dehydrate(self, bundle):
        obj = self.obj_get(code=bundle.data['code'])
        bundle.data['name'] = obj.get_code_display()
        return bundle


class AidTypeResource(ModelResource):
    class Meta:
        queryset = AidType.objects.all()
        include_resource_uri = False


class FinanceTypeResource(ModelResource):
    class Meta:
        queryset = FinanceType.objects.all()
        include_resource_uri = False


class TiedAidStatusTypeResource(ModelResource):
    class Meta:
        queryset = TiedAidStatusType.objects.all()
        include_resource_uri = False

    def dehydrate(self, bundle):
        obj = self.obj_get(code=bundle.data['code'])
        bundle.data['name'] = obj.get_code_display()
        return bundle