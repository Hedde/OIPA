# Django specific
from django.template.response import TemplateResponse


def docs_index(request):
    context = {}
    t = TemplateResponse(request, 'base.html', context)
    return t.render()

def docs_resources(request):
    context = {}
    t = TemplateResponse(request, 'documentation/resources.html', context)
    return t.render()

def docs_filtering(request):
    context = {}
    t = TemplateResponse(request, 'documentation/filtering.html', context)
    return t.render()

def docs_license(request):
    context = {}
    t = TemplateResponse(request, 'documentation/license.html', context)
    return t.render()