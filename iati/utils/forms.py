from django import forms
from utils.models import IATIXMLSource


class IATIXMLSourceForm(forms.ModelForm):
    class Meta:
        model = IATIXMLSource
