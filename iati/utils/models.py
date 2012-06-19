import os

# Django specific
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from StringIO import StringIO


class Publisher(models.Model):
    org_name = models.CharField(max_length=255)
    org_abbreviate = models.CharField(max_length=55, blank=True, null=True)

    def __unicode__(self):
        if self.org_abbreviate:
            return self.org_abbreviate
        return self.org_name

    class Meta:
        app_label = "utils"


def fix(value):
    return unicode(str(value).lower().replace(' ', '_'))

def get_upload_path(instance, filename):
    return os.path.join("utils", fix(instance.get_type_display()), fix(instance.publisher), fix(filename))

class IATIXMLSource(models.Model):
    TYPE_CHOICES = (
        (1, _(u"Activity Files")),
        (2, _(u"Organisation Files")),
    )
    ref = models.CharField(verbose_name=_(u"Reference"), max_length=55)
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    publisher = models.ForeignKey(Publisher)
    local_file = models.FileField(upload_to=get_upload_path, blank=True, null=True, editable=False)
    source_url = models.URLField(unique=True)

    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        app_label = "utils"

    def local_file_exists(self):
        if self.local_file:
            return "<img src='%sadmin/img/icon-yes.gif' alt='True'>" % settings.STATIC_URL
        return "<img src='%sadmin/img/icon-no.gif' alt='False'>" % settings.STATIC_URL
    local_file_exists.short_description = _(u"Local copy")
    local_file_exists.allow_tags = True

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
                    # python >= 2.7
                    import requests
                    r = requests.get(file_url)
                    f = StringIO(r.content)
                except ImportError:
                    # python <= 2.6
                    import urllib2
                    r = urllib2.urlopen(file_url)
                    f = r
                file = ContentFile(f.read(), self.ref)
                self.local_file = file
                super(IATIXMLSource, self).save(self, force_update=False, using=None)
            except ValidationError, e:
                pass