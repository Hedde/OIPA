from django.db import models


class IATIActivitySourceXML(models.Model):
    ref = models.CharField(max_length=55, unique=True)
    local_file = models.FileField(upload_to="utils/activity", blank=True, null=True)
    source_url = models.URLField()

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        app_label = "utils"
