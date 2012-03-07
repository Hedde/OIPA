import os, sys

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

sys.path.append('/var/lib/python-support/python2.5/django/')
sys.path.append('/home/iati/public_html/iati.com/iati-xal/')
sys.path.append('/home/iati/public_html/iati.com/iati-xal/iati/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'iati.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()