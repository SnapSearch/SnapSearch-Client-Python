.. snapsearch-client-python document
   :noindex:

Integration with WSGI Applications
==================================

Overview
--------

The `Pythonic SnapSearch Client`__ comes with a `WSGI`_-compliant Interceptor
Middleware for easy integration with existing web applications. The solution is
framework agnostic, and supports any `WSGI`_-compliant web applications, either
hand-made, or built upon `WSGI`_ framewrorks (such as Django_, Falcon_, Flask_,
web2py_, etc.).

.. __: https://github.com/SnapSearch/SnapSearch-Client-Python/
.. _WSGI: http://legacy.python.org/dev/peps/pep-3333/
.. _Django: https://www.djangoproject.com/
.. _Falcon: http://falconframework.org
.. _Flask: http://flask.pocoo.org/
.. _web2py: http://web2py.com/


Django App
----------

Django_ is a high-level Python Web framework best known for rapid development
of data-intensive web applications. To create a simple ``"Hello World"``
application,

1. start a ``hello_world`` project with ``django-admin.py``

.. code-block:: bash

    $ django-admin.py startproject hello_world

2. create a ``home`` view in ``hello_world/view.py``

.. code-block:: python

    from django.http import HttpResponse

    def home(request):
        return HttpResponse("Hello World!")

3. add the ``home`` view to ``hello_world/urls.py``

.. code-block:: python

    from django.conf.urls import patterns, include, url

    urlpatterns = patterns(
        '',
        url(r'^$', 'hello_world.views.home', name='home'),
    )

Integration
-----------

0. integration all happens in ``hello_world/wsgi.py``, the original content
   should look like,

.. code-block:: python

    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello_world.settings")

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()


1. initialize an ``Interceptor``.

.. code-block:: python

    from SnapSearch import Client, Detector, Interceptor
    interceptor = Interceptor(Client(api_email, api_key), Detector())


2. deploy the ``Interceptor``.

.. code-block:: python

    from SnapSearch.wsgi import InterceptorMiddleware
    application = InterceptorMiddleware(application, interceptor)


3. putting it all together.

.. code-block:: python

    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello_world.settings")

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    # API credentials
    api_email = "<email>"
    api_key = "<key>"

    # initialize the interceptor
    from SnapSearch import Client, Detector, Interceptor
    interceptor = Interceptor(Client(api_email, api_key), Detector())

    # deploy the interceptor
    from SnapSearch.wsgi import InterceptorMiddleware
    application = InterceptorMiddleware(application, interceptor)


Verification
------------

1. server servers the Django application at ``http://<server_ip>:5000/``.

.. code-block:: none

    # Apache server's virtual host configuration (partial)
    <VirtualHost *:5000>
        ServerName <server_name>
        CustomLog /<server_root>/log/access
        ...
        WSGIProcessGroup <server_name>
        WSGIDaemonProcess <server_name> python-path=/<server_root>/hello_world:/usr/lib/python2.6/site-packages:/usr/lib64/python2.6/site-packages display-name=%{GROUP}
        WSGIScriptAlias / /<server_root>/hello_world/wsgi.py
        DocumentRoot /<server_root>/hello_world/
        <Directory /<server_root>/hello_world>
            ...
        </Directory>
    </VirtualHost>

2. search engine robot visits (emulated with ``curl``),

.. code-block:: bash

    $ curl -i A "Googlebot" http://<server_ip>:5000/main.py

and receives an *intercepted* HTTP response

.. code-block:: none

    HTTP/1.1 200 OK
    Date: Thu, 13 Mar 2014 14:20:18 GMT
    Server: Apache/2.2.15 (CentOS)
    Connection: close
    Transfer-Encoding: chunked
    Content-Type: text/plain; charset=UTF-8

    <html><head><style type="text/css">body { background: #fff }</style></head><body>Hello World!</body></html>

3. server log shows both the robot and SnapSearch backend service.

.. code-block:: bash

    $ cat /<server_root>/log/access
    ...
    <robot_ip> - - [13/Mar/2014:22:20:19 +0800] "GET / HTTP/1.1" 200 14
    <snapsearch_ip> - - [13/Mar/2014:22:20:18 +0800] "GET / HTTP/1.1" 200 107
