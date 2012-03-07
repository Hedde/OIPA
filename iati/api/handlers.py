from piston.handler import BaseHandler, AnonymousBaseHandler
from django.core.exceptions import FieldError
from piston.utils import rc
from piston.resource import Resource
from django.db.models import ForeignKey
from django.db.models.query import QuerySet


class ResourceRegistrar(dict):

    def create_handler(self, model):
        meta = model._meta
        app_label = meta.app_label
        model_name = meta.object_name
        handler_name = '%sHandler' % model_name

        fields = {}
        for f in meta.fields:
            fields[f.name] = f.__class__.__name__

        doc = '''
API handler for <em>%s.%s</em> model.
For base usegae see describtion of <a href="#BaseApiHandler">BaseApiHandler</a>.
<span class="label notice">Fields:</span> %s
''' % (app_label, model_name, fields)

        class cls(BaseApiHandler):
            pass

        cls.model = model
        cls.__doc__ = doc
        cls.__name__ = handler_name

        return cls

    def register(self, *args):
        for handler in args:
            if issubclass(handler, BaseHandler):
                self[handler.model] = Resource(handler=handler)
            else:
                self.register(self.create_handler(handler))

resource_registrar = ResourceRegistrar()


class FieldsDescriptor(object):
    _cache = {}

    def __get__(self, obj, cls):
        if not cls in self._cache:
            fields = []
            for f in cls.model._meta.fields:
                if isinstance(f, ForeignKey):
                    fields.append(f.get_attname())
                else:
                    fields.append(f.name)
            self._cache[cls] = tuple(fields)

        return self._cache[cls]


class BaseApiHandler(BaseHandler):
    """
Base class for API handler.
For list of objects use <span class="label notice">RESOURCE URI</span> without <strong>{id}</strong>.

For ordering use <strong>?_order_by={field}</strong>. For descendant ordering use <strong>?_order_by=-{field}</strong>.
You can use ordering by multiple fields like: <strong>?_order_by={field1}&_order_by={field2}</strong>.

For filtering use <strong>?{field1}={value}&{field2}={value}</strong>.
You can use lookups for filtering supported by Django, see <a href="https://docs.djangoproject.com/en/1.3/ref/models/querysets/#field-lookups">documentation</a>.
Tested with <strong>gt, gte, lt, lte</strong> lookups.

You can user complex filters with AND or OR conditions:
?description__contains=Towards&title__contains=SALIN|title__contains=DHA
?description__contains=Towards&title__contains=SALIN|DHA
?description__contains=Towards&title__contains=SALIN|sector_code=15164
First and second are equal.

For date fields use "YYYY-MM-DD" format.
For datetime: "YYYY-MM-DD HH:MM:SS", "YYYY-MM-DD HH:MM" or "YYYY-MM-DD".
For example <strong>?created__gte=2011-10-10</strong>.

For ForeignKey use id: <strong>?organisation=1</strong>.
You can filter by related models names like <strong>?activity__title=DHA STD/leg. empowerment women</strong>

Default output format is JSON. But you can use other with:
XML - <strong>?emitter_format=xml</strong>
YAML - <strong>?emitter_format=yaml</strong>
    """
    allowed_methods = ('GET',)
    fields = FieldsDescriptor()

    @classmethod
    def resource_uri(cls, obj=None):
        app_label = cls.model._meta.app_label
        model_name = cls.model._meta.object_name.lower()

        if obj:
            return ('api:object', [app_label, model_name, obj.pk])
        else:
            return ('api:object', [app_label, model_name, '{id}'])

    def read(self, request, *args, **kwargs):
        ordering = kwargs.pop('_order_by', [])
        try:
            response = super(BaseApiHandler, self).read(request, *args, **kwargs)
        except FieldError, e:
            response = rc.BAD_REQUEST
            response.write(' ')
            response.write(e)
            return response

        if isinstance(response, QuerySet) and ordering:
            response = response.order_by(*ordering)

        return response