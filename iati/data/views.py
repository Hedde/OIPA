from utils.decorators import render_to
from django.conf import settings

@render_to('main/index.html')
def index(request):
    return {}