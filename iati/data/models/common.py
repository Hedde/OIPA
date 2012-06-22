# Django specific
from django.db import models
from django.utils.translation import ugettext_lazy as _

# App specific
from data.models.constants import BUDGET_TYPE_CHOICES
from data.models.constants import COUNTRIES_TUPLE
from data.models.constants import FLOW_TYPE_CHOICES
from data.models.constants import FLOW_TYPE_CHOICES_MAP
from data.models.constants import POLICY_SIGNIFICANCE_CHOICES
from data.models.constants import REGION_CHOICES
from data.models.constants import TIED_AID_STATUS_CHOICES
from data.models.constants import VOCABULARY_CHOICES


class Language(models.Model):
    code = models.CharField(max_length=55)

    class Meta:
        app_label = "data"


class Country(models.Model):
    iso = models.CharField(max_length=2, primary_key=True, choices=COUNTRIES_TUPLE)

    def __unicode__(self):
        return "%s - %s" % (self.iso, self.get_iso_display())

    class Meta:
        app_label = "data"
        verbose_name = _("country")
        verbose_name_plural = _("countries")


class Region(models.Model):
    code = models.CharField(max_length=5, primary_key=True, choices=REGION_CHOICES)

    def __unicode__(self):
        return "%s - %s" % (self.code, self.get_code_display())

    class Meta:
        app_label = "data"


class CommonType(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class VocabularyType(models.Model):
    code = models.CharField(max_length=15, primary_key=True, choices=VOCABULARY_CHOICES)

    class Meta:
        app_label = "data"


class SignificanceType(models.Model):
    code = models.IntegerField(max_length=5, primary_key=True, choices=POLICY_SIGNIFICANCE_CHOICES)

    class Meta:
        app_label = "data"


class CollaborationType(models.Model):
    code = models.CharField(max_length=55, primary_key=True)

    class Meta:
        app_label = "data"


class FlowType(models.Model):
    code = models.IntegerField(max_length=5, primary_key=True, choices=FLOW_TYPE_CHOICES)

    class Meta:
        app_label = "data"


class FinanceType(models.Model):
    code = models.IntegerField(max_length=5, primary_key=True)

    class Meta:
        app_label = "data"


class AidType(models.Model):
    code = models.CharField(max_length=5, primary_key=True)

    class Meta:
        app_label = "data"


class TiedAidStatusType(models.Model):
    code = models.IntegerField(max_length=5, primary_key=True, choices=TIED_AID_STATUS_CHOICES)

    class Meta:
        app_label = "data"


class CurrencyType(CommonType):
    language = models.ForeignKey(Country, blank=True, null=True)

    class Meta:
        app_label = "data"


class ActivityStatusType(models.Model):
    code = models.IntegerField(max_length=8, unique=True, blank=True, null=True)
    name = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(Country, blank=True, null=True)

    class Meta:
        app_label = "data"


class Sector(models.Model):
    code = models.CharField(max_length=55)
    vocabulary_type = models.ForeignKey(VocabularyType, blank=True, null=True)

    class Meta:
        abstract = True


class Budget(models.Model):
    period_start = models.DateField()
    period_end = models.DateField()
    value = models.FloatField()
    type = models.IntegerField(max_length=2, choices=BUDGET_TYPE_CHOICES, blank=True, null=True)
    currency = models.ForeignKey(CurrencyType, blank=True, null=True)

    class Meta:
        app_label = "data"


class Contact(models.Model):
    organisation = models.CharField(max_length=255, blank=True, null=True)
    person_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    mailing_address = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Document(models.Model):
    """
    @url        The target URL of the external document, e.g. "http://www.example.org/doc.html".
    @format     The MIME type of the external document, e.g. "application/pdf". A partial list of MIME types
                appears at http://iatistandard.org/codelists/file_format
    @language   The ISO 639 language code for the target document, e.g. "en".
    """
    url = models.URLField()
    format = models.CharField(max_length=55)
    language = models.ForeignKey(Language)

    class Meta:
        abstract = True


class Website(models.Model):
    url = models.URLField()

    class Meta:
        abstract = True