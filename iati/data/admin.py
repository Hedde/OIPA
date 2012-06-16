from django.contrib import admin
from data.models.organisation import Organisation, RecipientCountryBudget, RecipientOrgBudget, TotalBudget,\
    Activity, Transaction, PolicyMarker, ParticipatingOrganisation,IATISet
from data.models.common import Sector


admin.site.register(Sector)


class PolicyMarkerAdmin(admin.ModelAdmin):
    list_display = ['activity', 'description', 'vocabulary', 'significance', 'code']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['activity', 'transaction_type', 'provider_org', 'receiver_org', 'value', 'value_date']


class ParticipatingOrganisationInline(admin.TabularInline):
    model = ParticipatingOrganisation


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'organisation', 'title', 'total_budget', 'recipient_country_code', 'last_updated']
    inlines = [ParticipatingOrganisationInline]


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'default_currency', 'ref', 'last_updated']


class RecipientCountryBudgetAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'period_start', 'period_end', 'value', 'country_code', 'country_name']


class RecipientOrgBudgetAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'period_start', 'period_end', 'value', 'recipient_org', 'recipient_ref']


class TotalBudgetAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'period_start', 'period_end', 'value']

admin.site.register(PolicyMarker, PolicyMarkerAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(TotalBudget, TotalBudgetAdmin)
admin.site.register(RecipientOrgBudget, RecipientOrgBudgetAdmin)
admin.site.register(RecipientCountryBudget, RecipientCountryBudgetAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(IATISet)