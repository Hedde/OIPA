# Django specific
from django.db import models
from django.utils.translation import ugettext_lazy as _

# App specific
from data.models.constants import COUNTRIES_TUPLE
from data.models.constants import REGION_CHOICES
from data.models.constants import TYPE_CHOICES


class Country(models.Model):
    iso = models.CharField(max_length=2, primary_key=True, choices=COUNTRIES_TUPLE)

    def __unicode__(self):
        return "%s - %s" % (self.iso, self.get_iso_display())

    class Meta:
        app_label = "data"
        verbose_name = _("country")
        verbose_name_plural = _("countries")


class Region(models.Model):
    """
    @code       Machine-readable code for the entity being described.
    @percentage The percentage of the project allocated to this geopolitical region, if known.
                Content must be a positive integer between 1 and 100, with no percentage sign.
    """
    code = models.CharField(max_length=5, primary_key=True, choices=REGION_CHOICES)

    def __unicode__(self):
        return "%s - %s" % (self.code, self.get_code_display())

    class Meta:
        app_label = "data"


class Organisation(models.Model):
    """
    @ref        Machine-readable identification string for the business object being described.
    @type       Free text describing the type of thing being referenced
    @org-name   The name of the organisation
    """
    ref = models.CharField(max_length=255)
    type = models.IntegerField(choices=TYPE_CHOICES, blank=True, null=True)
    org_name = models.CharField(max_length=255)
    org_name_lang = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = "data"


class CommonType(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class VocabularyType(CommonType):
    class Meta:
        app_label = "data"


class SignificanceType(CommonType):
    class Meta:
        app_label = "data"


class CollaborationType(CommonType):
    class Meta:
        app_label = "data"


class FlowType(CommonType):
    class Meta:
        app_label = "data"


class AidType(CommonType):
    class Meta:
        app_label = "data"


class FinanceType(CommonType):
    class Meta:
        app_label = "data"


class TiedAidStatusType(CommonType):
    class Meta:
        app_label = "data"


class CurrencyType(CommonType):
    language = models.ForeignKey(Country, blank=True, null=True)

    class Meta:
        app_label = "data"


class ActivityStatusType(CommonType):
    language = models.ForeignKey(Country, blank=True, null=True)

    class Meta:
        app_label = "data"


class BudgetType(CommonType):
    language = models.ForeignKey(Country, blank=True, null=True)

    class Meta:
        app_label = "data"


class Sector(models.Model):
    """
    @code       Machine-readable code for the entity being described.
    @vocabulary An identifier for the vocabulary in use, to segment sectors into different vocabularies
                (e.g. DAC, OCHA) to aid with comparison and classification. If omitted, assume DAC.
                See http://iatistandard.org/codelists/vocabulary
    """
    code = models.IntegerField(max_length=5)
    vocabulary_type = models.ForeignKey(VocabularyType, blank=True, null=True)

    class Meta:
        abstract = True


class Budget(BudgetType):
    period_start = models.DateField()
    periode_end = models.DateField()
    type = models.ForeignKey(BudgetType, related_name='budget_type')
    currency = models.ForeignKey(CurrencyType)

    class Meta:
        app_label = "data"


class Address(models.Model):
    street_name = models.CharField(max_length=255, blank=True, null=True)
    street_number = models.IntegerField(blank=True, null=True)
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)

    class Meta:
        app_label = "data"


class Contact(models.Model):
    organisation = models.CharField(max_length=255, blank=True, null=True)
    person_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(Address, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

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
    language = models.CharField(max_length=5)

    class Meta:
        abstract = True


class Website(models.Model):
    url = models.URLField()

    class Meta:
        abstract = True