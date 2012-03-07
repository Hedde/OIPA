from django.http import HttpResponse, Http404
from django.db.models.loading import get_model
from api.handlers import resource_registrar
from piston.utils import rc
from django.core.exceptions import ValidationError
from django.db.models import Q
from data.models import IATISet


def api(request, app_label, model_name, id=None):
    model = get_model(app_label, model_name)

    if not model:
        raise Http404

    resource = resource_registrar.get(model)

    if not resource:
        raise Http404

    if id:
        return resource(request, id=id)
    else:
        try:
            filters = _get_filters(request, resource)
            ordering = _get_ordering(request, resource)
        except ValidationError, e:
            response = rc.BAD_REQUEST
            response.write(e)
            return response

        return resource(request, _order_by=ordering, *filters)


def _get_filters(request, resource):
    resource.handler.model

    filters = []

    def parse_filter(name, value):
        if '|' in value:
            items = value.split('|')
            f = Q(**{str(name): items[0]})  # first is value for field from GET

            for item in items[1:]:
                params = item.split('=')
                if len(params) == 1:
                    fname = name
                    value = params[0]
                else:
                    fname = params[0]
                    value = u''.join(params[1:])

                f |= Q(**{str(fname): value})

            filters.append(f)
        else:
            filters.append(Q(**{str(name): value}))

    for name, value in request.GET.items():
        if not name.startswith('_'):
            for value in request.GET.getlist(name):
                parse_filter(name, value)

    return filters


def _get_ordering(request, resource):
    model = resource.handler.model
    ordering = request.GET.getlist('_order_by')
    field_names = [f.name for f in model._meta.fields]

    for field in ordering:
        if field.startswith('-'):
            field = field[1:]

        if not field in field_names:
            raise ValidationError(u'Model "%s" has not field "%s"' % (model._meta.object_name, field))

    return ordering

def last_updated(request):
    last_updated = IATISet.objects.get(organisation='Dutch Government').last_updated
    return HttpResponse(unicode(last_updated))