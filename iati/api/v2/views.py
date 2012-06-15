from django.http import HttpResponse
from django.template.response import TemplateResponse

def docs(request):
    context = {}
    t = TemplateResponse(request, 'documentation_v2.html', context)
    return t.render()