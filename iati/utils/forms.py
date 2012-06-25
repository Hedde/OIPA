# Django specific
from django import forms

# App specific
from utils.models import IATIXMLSource


class IATIXMLSourceForm(forms.ModelForm):
    class Meta:
        model = IATIXMLSource
