# Django specific
from django.contrib import admin

# App specific
from utils.models import IATIXMLSource



class IATIXMLSourceAdmin(admin.ModelAdmin):
    list_display = ['ref', 'type', 'local_file', 'source_url', 'date_created', 'date_updated']

admin.site.register(IATIXMLSource, IATIXMLSourceAdmin)