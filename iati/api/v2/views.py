# Django specific
from django.template.response import TemplateResponse


def docs_index(request):
    context = {}
    t = TemplateResponse(request, 'base.html', context)
    return t.render()