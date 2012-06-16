# Django specific
from django.db import models
from django.utils.translation import ugettext_lazy as _

# App specific
from data.models.constants import COUNTRIES_TUPLE
from data.models.constants import REGION_CHOICES
from data.models.constants import TYPE_CHOICES


class Country(models.Model):
    iso = models.CharField(max_length=2, primary_key=True, choices=COUNTRIES_TUPLE)

    class Meta:
        app_label = "users"
        verbose_name = _("country")
        verbose_name_plural = _("countries")

    def __unicode__(self):
        return "%s - %s" % (self.iso, self.get_iso_display())


class Region(models.Model):
    """
    @code	    Machine-readable code for the entity being described.
    @percentage	The percentage of the project allocated to this geopolitical region, if known.
                Content must be a positive integer between 1 and 100, with no percentage sign.
    """
    code = models.CharField(max_length=5, primary_key=True, choices=REGION_CHOICES)

    def __unicode__(self):
        return "%s - %s" % (self.code, self.get_code_display())


class Sector(models.Model):
    """
    @code	    Machine-readable code for the entity being described.
    @vocabulary	An identifier for the vocabulary in use, to segment sectors into different vocabularies
                (e.g. DAC, OCHA) to aid with comparison and classification. If omitted, assume DAC.
                See http://iatistandard.org/codelists/vocabulary
    @percentage	The percentage of the project allocated to this sector, if known. Content must be a positive
                integer between 1 and 100, with no percentage sign. Percentages are comparable only across
                sectors in the same vocabulary.
    """
    code = models.IntegerField(max_length=5)
    vocabulary = models.CharField(max_length=12, choices=REGION_CHOICES)
    percentage = models.IntegerField()


class ReportingOrganisation(models.Model):
    """
    @ref	    Machine-readable identification string for the business object being described.
    @type	    Free text describing the type of thing being referenced
    @org-name	The name of the organisation
    """
    ref = models.CharField(max_length=255)
    type = models.IntegerField(choices=TYPE_CHOICES)
    org_name = models.CharField(max_length=255)
    org_name_lang = models.CharField(max_length=255)


class Address(models.Model):
    street_name = models.CharField(max_length=255, blank=True, null=True)
    street_number = models.IntegerField(blank=True, null=True)
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)


class Contact(models.Model):
    organisation = models.CharField(max_length=255, blank=True, null=True)
    person_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(Address, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)