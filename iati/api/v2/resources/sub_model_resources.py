# Tastypie specific
from tastypie.resources import ModelResource

# Data specific
from data.models.activity import IATIActivityCountry
from data.models.activity import IATIActivityRegion
from data.models.common import ActivityStatusType


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