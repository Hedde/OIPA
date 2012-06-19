# Django specific
from django.contrib import admin

# App specific
from utils.models import IATIXMLSource, Publisher



class IATIXMLSourceAdmin(admin.ModelAdmin):
    list_display = ['ref', 'publisher', 'type', 'local_file_exists', 'date_created', 'date_updated']
    list_filter = ('publisher', 'type')

admin.site.register(Publisher)
admin.site.register(IATIXMLSource, IATIXMLSourceAdmin)