from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from utils.forms import IATIActivitySourceXMLForm
from utils.models import IATIActivitySourceXML


class JSONResponse(HttpResponse):
    def __init__(self, data):
        output = simplejson.dumps(data)
        super(JSONResponse, self).__init__(output, mimetype="text/javascript")

def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer


def render_json(func):
    def wrapper(request, *args, **kw):
        data = func(request, *args, **kw)
        if isinstance(data, HttpResponse):
            return data
        return JSONResponse(data)
    return wrapper


@login_required
def upload_activity_set(request):

    form_class = IATIActivitySourceXMLForm
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # ...
        else:
            pass
            # ...
    else:
        form = form_class()
    return render_to_response("upload.html", {
        "form": form,
        "sets": IATIActivitySourceXML.objects.all()
        }, context_instance=RequestContext(request))


#    name = request.GET.get('name')
#    xml = request.GET.get('xml')
#    if name and xml:
#        grab_it(name, "b", xml)
#        return HttpResponse('Success')
#
#    # Dutch organisation set
#    #    url = 'http://www.minbuza.nl/binaries/content/assets/minbuza/nl/services/opendata/iati_organisation.xml/iati_organisation.xml/hippogallery%3Aasset'
#    # Dutch activity set
#    #    url = 'http://www.minbuza.nl/binaries/content/assets/minbuza/nl/services/opendata/iati_activities.xml/iati_activities.xml/hippogallery%3Aasset'
#    #    url = 'http://siteresources.worldbank.org/IATI/WB-ZA.xml'
#    #    grab_it('iati_activities_wb_south_africa.xml',"b",url)
#
#    return HttpResponse('No set provided')