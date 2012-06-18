# Django specific
from django.db import models

# App specific
from data.models.constants import TYPE_CHOICES


class Organisation(models.Model):
    ref = models.CharField(max_length=255)
    type = models.IntegerField(choices=TYPE_CHOICES, blank=True, null=True)
    org_name = models.CharField(max_length=255)
    org_name_lang = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = "data"


class ParticipatingOrganisation(models.Model):
    """
    Note: participationOrg field NOT YET described in activity standaard
    """
    iati_activity = models.ForeignKey('IATIActivity') # import as string to avoid import circle
    name = models.CharField(max_length=500)
    role = models.CharField(max_length=500)
    type = models.CharField(max_length=250)
    ref = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "data"