# Django specific
from django.db import models
from django.utils.translation import ugettext_lazy as _

# App specific
from data.models.common import Contact
from data.models.common import Country
from data.models.common import Language
from data.models.common import CollaborationType
from data.models.common import FlowType
from data.models.common import AidType
from data.models.common import FinanceType
from data.models.common import TiedAidStatusType
from data.models.common import SignificanceType
from data.models.common import VocabularyType
from data.models.common import ActivityStatusType
from data.models.common import Region
from data.models.common import Sector
from data.models.common import Document
from data.models.common import Website
from data.models.common import Budget
from data.models.common import CurrencyType
from data.models.common import Transaction
from data.models.organisation import Organisation
from data.models.constants import DESCRIPTION_TYPE_CHOICES
from data.models.constants import DISBURSEMENT_CHANNEL_CHOICES
from data.models.constants import POLICY_MARKER_CODE_CHOICES
from data.models.constants import RELATED_CHOICES
from data.models.constants import TIED_AID_STATUS_CHOICES
from data.models.constants import TRANSACTION_TYPE_CHOICES


class IATIActivity(models.Model):
    iati_identifier = models.CharField(max_length=50, primary_key=True)
    reporting_organisation = models.ForeignKey(Organisation, to_field='ref')

    activity_status = models.ForeignKey(ActivityStatusType, blank=True, null=True)

    start_planned = models.DateField(blank=True, null=True)
    start_actual = models.DateField(blank=True, null=True)
    end_planned = models.DateField(blank=True, null=True)
    end_actual = models.DateField(blank=True, null=True)

    # TODO: Sub-national Geographic Location
    # TODO: Performance

    collaboration_type = models.ForeignKey(CollaborationType, blank=True, null=True)
    default_flow_type = models.ForeignKey(FlowType, blank=True, null=True)
    default_aid_type = models.ForeignKey(AidType, blank=True, null=True)
    default_finance_type = models.ForeignKey(FinanceType, blank=True, null=True)
    default_tied_status_type = models.ForeignKey(TiedAidStatusType, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(editable=False)

    def __unicode__(self):
        return self.iati_identifier

    class Meta:
        app_label = "data"
        verbose_name_plural = _(u"IATIActivities")


class IATIActivityTitle(models.Model):
    iati_activity = models.ForeignKey(IATIActivity)
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language, blank=True, null=True)

    class Meta:
        app_label = "data"


class IATIActivityDescription(models.Model):
    iati_activity = models.ForeignKey(IATIActivity)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=2, choices=DESCRIPTION_TYPE_CHOICES, blank=True, null=True)
    language = models.ForeignKey(Language, blank=True, null=True)

    class Meta:
        app_label = "data"


class OtherIdentifier(models.Model):
    """
    @owner-ref      An identifier for the owner of this identifier, in URI format. See the list of
                    officially-registered organizations at http://iatistandard.org/codelists/organisation
    @owner-name
    """
    iati_activity = models.ForeignKey(IATIActivity)
    owner_ref = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)


class IATIActivityRegion(models.Model):
    iati_activity = models.ForeignKey(IATIActivity)
    region = models.ForeignKey(Region)
    percentage = models.IntegerField(blank=True, null=True)

    class Meta:
        app_label = "data"


class IATIActivityCountry(models.Model):
    iati_activity = models.ForeignKey(IATIActivity)
    country = models.ForeignKey(Country)
    percentage = models.IntegerField(blank=True, null=True)

    class Meta:
        app_label = "data"


class IATIActivitySector(Sector):
    iati_activity = models.ForeignKey(IATIActivity)
    percentage = models.IntegerField(blank=True, null=True)

    class Meta:
        app_label = "data"


class IATITransaction(Transaction):
    """
    If omitted, the provider organisation is the reporting organisation
    """
    iati_activity = models.ForeignKey(IATIActivity)

    class Meta:
        app_label = "data"


class IATIActivityBudget(Budget):
    iati_activity = models.ForeignKey(IATIActivity)

    class Meta:
        app_label = "data"


class PlannedDisbursement(models.Model):
    iati_activity = models.ForeignKey(IATIActivity)
    period_start = models.DateField()
    period_end = models.DateField()
    currency = models.ForeignKey(CurrencyType)

    class Meta:
        app_label = "data"


class RelatedActivity(models.Model):
    """
    @ref    Machine-readable identification string for the business object being described.
    @type   Free text describing the type of thing being referenced.
    """
    ref = models.IntegerField(choices=RELATED_CHOICES)
    type = models.TextField()


class IATIActivityContact(Contact):
    iati_activity = models.ForeignKey(IATIActivity)

    class Meta:
        app_label = "data"


class IATIActivityDocument(Document):
    iati_activity = models.ForeignKey(IATIActivity)

    class Meta:
        app_label = "data"


class IATIActivityWebsite(Website):
    iati_activity = models.ForeignKey(IATIActivity)

    class Meta:
        app_label = "data"


class IATIActivityPolicyMarker(models.Model):
    iati_activity = models.ForeignKey(IATIActivity)
    code = models.IntegerField(max_length=5, choices=POLICY_MARKER_CODE_CHOICES)
    vocabulary_type = models.ForeignKey(VocabularyType, blank=True, null=True)
    significance_type = models.ForeignKey(SignificanceType, blank=True, null=True)

    class Meta:
        app_label = "data"