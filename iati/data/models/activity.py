# Django specific
from django.db import models
from django.utils.translation import ugettext_lazy as _

# App specific
from data.models.common import Contact
from data.models.common import Country
from data.models.common import Region
from data.models.common import ReportingOrganisation
from data.models.common import Sector
from data.models.constants import RELATED_CHOICES
from data.models.constants import TRANSACTION_TYPE_CHOICES


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

    recipient_country = models.ForeignKey(Country, blank=True, null=True) # **
    recipient_region = models.ForeignKey(Region, blank=True, null=True) # **
    # TODO: Sub-national Geographic Location
    percentage = models.IntegerField(blank=True, null=True) # **

    sector = models.ForeignKey(Sector)

    collaboration_type = models.CharField(max_length=500, blank=True, null=True)
    collaboration_type_code = models.CharField(max_length=50, blank=True, null=True)
    default_flow_type = models.CharField(max_length=500, blank=True, null=True)
    default_flow_type_code = models.CharField(max_length=50, blank=True, null=True)
    default_aid_type = models.CharField(max_length=500, blank=True, null=True)
    default_aid_type_code = models.CharField(max_length=50, blank=True, null=True)
    default_finance_type = models.CharField(max_length=500, blank=True, null=True)
    default_finance_code = models.CharField(max_length=50, blank=True, null=True)
    default_tied_status = models.CharField(max_length=500, blank=True, null=True)
    default_tied_status_code = models.CharField(max_length=50, blank=True, null=True)
    activity_status = models.CharField(max_length=500, blank=True, null=True)
    activity_status_code = models.CharField(max_length=50, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.iati_identifier

    class Meta:
        app_label = "data"
        verbose_name_plural = _(u"IATIActivities")


class Transaction(models.Model):
    iati_activity = models.ForeignKey(IATIActivity)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE_CHOICES)
    provider_org = models.CharField(max_length=250)
    receiver_org = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    value_date = models.DateField()
    transaction_date = models.DateField()

    class Meta:
        app_label = "data"


class RelatedActivity(models.Model):
    """
    @ref    Machine-readable identification string for the business object being described.
    @type   Free text describing the type of thing being referenced.
    """
    ref = models.IntegerField(choices=RELATED_CHOICES)
    type = models.TextField()


class Document(models.Model):
    """
    @url        The target URL of the external document, e.g. "http://www.example.org/doc.html".
    @format     The MIME type of the external document, e.g. "application/pdf". A partial list of MIME types
                appears at http://iatistandard.org/codelists/file_format
    @language   The ISO 639 language code for the target document, e.g. "en".
    """
    iati_activity = models.ForeignKey(IATIActivity)
    url = models.URLField()
    format = models.CharField(max_length=55)
    language = models.CharField(max_length=5)


class Website(models.Model):
    iati_activity = models.ForeignKey(IATIActivity)
    url = models.URLField()