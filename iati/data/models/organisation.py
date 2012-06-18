# Django specific
from django.db import models

# App specific
from data.models.constants import ORGANISATION_TYPE_CHOICES


class Organisation(models.Model):
    ref = models.CharField(max_length=50)
    type = models.IntegerField(choices=ORGANISATION_TYPE_CHOICES, blank=True, null=True)
    org_name = models.CharField(max_length=255)
    org_name_lang = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = "data"


class ParticipatingOrganisation(Organisation):
    """
    Note: participationOrg field NOT YET described in activity standaard
    """
    iati_activity = models.ForeignKey('IATIActivity') # import as string to avoid import circle
    role = models.CharField(max_length=500)

    def __unicode__(self):
        return self.org_name

    class Meta:
        app_label = "data"