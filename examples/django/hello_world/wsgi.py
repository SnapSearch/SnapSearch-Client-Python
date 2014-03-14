import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello_world.settings")

# django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# load SnapSearch API credentials
api_email = "<email>"
api_key = "<key>"

# initialize the interceptor
from SnapSearch import Client, Detector, Interceptor
interceptor = Interceptor(Client(api_email, api_key), Detector())

# deploy the interceptor
from SnapSearch.wsgi import InterceptorMiddleware
application = InterceptorMiddleware(application, interceptor)
