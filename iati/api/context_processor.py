# Django specifiek
from django.conf import settings


def version(request):
    """
    Latest stable API version
    """
    return dict(version=settings.API_VERSION)
