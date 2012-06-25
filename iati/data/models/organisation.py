# Django specific
from django.db import models

# App specific
from data.models.constants import ORGANISATION_TYPE_CHOICES


class Organisation(models.Model):
    ref = models.CharField(max_length=25, primary_key=True)
    type = models.IntegerField(choices=ORGANISATION_TYPE_CHOICES, blank=True, null=True)
    org_name = models.CharField(max_length=255)
    org_name_lang = models.CharField(max_length=255, blank=True, null=True)

    date_created = models.DateField(auto_now_add=True, editable=False)
    date_updated = models.DateField(auto_now=True, editable=False)

    class Meta:
        app_label = "data"


class ParticipatingOrganisation(models.Model):
    """
    Note: participationOrg field NOT YET described in activity standaard
    """
    iati_activity = models.ForeignKey('IATIActivity') # import as string to avoid import circle
    ref = models.CharField(max_length=25)
    type = models.IntegerField(choices=ORGANISATION_TYPE_CHOICES, blank=True, null=True)
    org_name = models.CharField(max_length=255)
    org_name_lang = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=500)

    date_created = models.DateField(auto_now_add=True, editable=False)
    date_updated = models.DateField(auto_now=True, editable=False)

    def __unicode__(self):
        return self.org_name

    class Meta:
        app_label = "data"