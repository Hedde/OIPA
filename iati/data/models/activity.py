# Django specific
from django.db import models
from django.utils.translation import ugettext_lazy as _

# App specific
from data.models.common import ReportingOrganisation, Contact



class RecipientCountry(models.Model):
    pass


class IATIActivity(models.Model):
    iati_identifier = models.CharField(max_length=50, unique=True)
    reporting_organistion = models.ForeignKey(ReportingOrganisation)

    title = models.CharField(max_length=255)
    description = models.TextField()
    activity_status = models.CharField(max_length=500, blank=True, null=True)
    activity_status_code = models.CharField(max_length=50, blank=True, null=True)

    start_planned = models.DateField(blank=True, null=True)
    start_actual = models.DateField(blank=True, null=True)
    end_planned = models.DateField(blank=True, null=True)
    end_actual = models.DateField(blank=True, null=True)

    activity_contact = models.ForeignKey(Contact, blank=True, null=True)

    class Meta:
        app_label = "data"
        verbose_name_plural = _(u"IATIActivities")