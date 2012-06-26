# Django specific
from django.template.response import TemplateResponse
from api.v2.resources.model_resources import ActivityResource
from api.v2.resources.model_resources import OrganisationResource


def docs_index(request):
    context = dict()
    context['title'] = 'Documentation'
    t = TemplateResponse(request, 'base.html', context)
    return t.render()

def docs_start(request):
    context = dict()
    context['title'] = 'Getting started'
    t = TemplateResponse(request, 'documentation/start.html', context)
    return t.render()

def docs_resources(request):
    context = dict()
    context['title'] = 'Resources'
    context['resources'] = dict(
        organisation = OrganisationResource.__name__,
        organisation_doc = OrganisationResource.__doc__,
        activity = ActivityResource.__name__,
        activity_doc = ActivityResource.__doc__
    )
    t = TemplateResponse(request, 'documentation/resources.html', context)
    return t.render()

def docs_filtering(request):
    context = dict()
    context['title'] = 'Filtering'
    t = TemplateResponse(request, 'documentation/filtering.html', context)
    return t.render()