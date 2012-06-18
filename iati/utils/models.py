import os

# Django specific
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import ugettext_lazy as _

from StringIO import StringIO



def fix(value):
    return unicode(str(value).lower().replace(' ', '_'))

def get_upload_path(instance, filename):
    return os.path.join("utils", fix(instance.get_type_display()), fix(instance.publisher), fix(filename))

class IATIXMLSource(models.Model):
    TYPE_CHOICES = (
        (1, _(u"Activity Files")),
        (2, _(u"Organisation Files")),
    )
    ref = models.CharField(verbose_name=_(u"Reference"), max_length=55, unique=True)
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    publisher = models.CharField(max_length=100)
    local_file = models.FileField(upload_to=get_upload_path, blank=True, null=True, editable=False)
    source_url = models.URLField()

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        app_label = "utils"

    def get_absolute_url(self):
        return "/media/%s" % self.local_file

    def save(self, force_insert=False, force_update=False, using=None):
        # TODO: implement changes/updates
        if self.ref and self.source_url:
            if not self.ref[4:] == ".xml":
                self.ref += ".xml"
            file_url = self.source_url
            try:
                try:
                    # python 2.7
                    import requests
                    r = requests.get(file_url)
                    f = StringIO(r.content)
                except ImportError:
                    # python 2.6
                    import urllib2
                    r = urllib2.urlopen(file_url)
                    f = StringIO(r)
                file = ContentFile(f.read(), self.ref)
                self.local_file = file
                super(IATIXMLSource, self).save(self, force_update=False, using=None)
            except ValidationError, e:
                pass