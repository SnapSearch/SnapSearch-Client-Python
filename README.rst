.. snapsearch-client-python document
   :noindex:

========================
SnapSearch Client Python
========================

.. image:: https://travis-ci.org/SnapSearch/SnapSearch-Client-Python.png?branch=master
   :target: https://travis-ci.org/SnapSearch/SnapSearch-Client-Python

.. image:: http://badge.fury.io/py/snapsearch-client-python.png
   :target: http://badge.fury.io/py/snapsearch-client-python

.. image:: https://pypip.in/d/snapsearch-client-python/badge.png
   :target: https://crate.io/packages/snapsearch-client-python/
   :alt: Downloads

.. image:: https://pypip.in/license/snapsearch-client-python/badge.png
   :target: https://pypi.python.org/pypi/snapsearch-client-python/
   :alt: License

SnapSearch Client Python is a Python based framework agnostic HTTP client
library for SnapSearch (https://snapsearch.io/).

SnapSearch provides similar libraries in other languages:
https://github.com/SnapSearch/SnapSearch-Clients


Installation
============

The Pythonic ``snapsearch-client`` requires a dependable HTTP library that can
verify SSL certificates for HTTPS requests. Normally, this means you need to
have either `requests`_ or `PycURL`_.

.. _`PycURL`: http://pycurl.sourceforge.net/
.. _`requests`: http://python-requests.org/

To install with ``pip``, simply:

.. code-block:: bash

    $ pip install snapsearch-client-python

Or, if you prefer ``easy_install``:

.. code-block:: bash

    $ easy_install snapsearch-client-python


Usage
=====

The `Pythonic SnapSearch Client`_ provides `WSGI`_ and `CGI`_ middlewares for
integrating SnapSearch with respective Python Web applications. There are also
framework agnostic core objects that can be used independently.

.. _`Pythonic SnapSearch Client`: https://github.com/SnapSearch/SnapSearch-Client-Python
.. _`WSGI`: http://legacy.python.org/dev/peps/pep-3333/
.. _`CGI`: http://docs.python.org/library/cgi.html

The following examples include step-by-step instructions on the context of
using the `Pythonic SnapSearch Client`_ in your Python web applications.

- `Integration with WSGI Applications I (Flask) <https://pythonhosted.org/snapsearch-client-python/flask.html>`_
- `Integration with WSGI Applications II (Django) <https://pythonhosted.org/snapsearch-client-python/django.html>`_
- `Integration with Python CGI Scripts <https://pythonhosted.org/snapsearch-client-python/pycgi.html>`_

For full documentation on the API and API request parameters see:
https://snapsearch.io/documentation


Basic Usage
-----------

The below instructions is an abridged version of the Flask_ example. The
following python script serves a simple ``"Hello World"`` page through any of
the public IP address(es) of the runner machine.

.. _Flask: http://flask.pocoo.org/

.. code:: python

    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return "Hello World!\r\n"

    if __name__ == '__main__':
        app.run(host="0.0.0.0", port=5000)

To start the application,

.. code-block:: bash

    $ pip install Flask
    $ pip install snapsearch-client-python
    $ python main.py
     * Running on http://0.0.0.0:5000/

To enable SnapSearch-based interception for this application,

1. initialize an ``Interceptor``.

.. code-block:: python

    from SnapSearch import Client, Detector, Interceptor
    interceptor = Interceptor(Client(api_email, api_key), Detector())


2. deploy the ``Interceptor``.

.. code-block:: python

    from SnapSearch.wsgi import InterceptorMiddleware
    app.wsgi_app = InterceptorMiddleware(app.wsgi_app, interceptor)


3. putting it all together.

.. code-block:: python

    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return "Hello World!\r\n"

    if __name__ == '__main__':
        # API credentials
        api_email = "<email>"  # change this to the registered email
        api_key = "<key>"  # change this to the real api credential

        # initialize the interceptor
        from SnapSearch import Client, Detector, Interceptor
        interceptor = Interceptor(Client(api_email, api_key), Detector())

        # deploy the interceptor
        from SnapSearch.wsgi import InterceptorMiddleware
        app.wsgi_app = InterceptorMiddleware(app.wsgi_app, interceptor)

        # start servicing
        app.run(host="0.0.0.0", port=5000)


Advanced Topics
---------------

Customizing the ``Detector``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Detector`` class can take ``ignored_routes`` and ``matched_routes`` as
optional arguments to its constructor and perform interception detection in a
per-route basis. For example, the following ``detector`` will bypass
interception for any access to ``http://<server_name>/ignored.*``, and enforce
interception for any access to ``http://<server_name>/matched.*``.

.. code-block:: python

        from SnapSearch import Detector
        detector = Detector(ignored_routes=["^\/ignored", ],
                            matched_routes=["^\/matched", ])

The ``Detector`` class can take external ``robots.json`` and ``extensions.json``
files as optional arguments to its constructor. Namely,

.. code-block:: python

    from SnapSearch import Detector
    detector = Detector(robots_json="path/to/external/robots.json",
                        extensions_json="path/to/external/extensions.json")

You can also modify the lists of robots and extension through the ``robots``
and ``extensions`` properties of the ``detector`` object. For example,
the following customization will bypass interception for ``Googlebot``.

.. code-block:: python

    from SnapSearch import Detector
    detector = Detector(robots_json="path/to/external/robots.json",
                        extensions_json="path/to/external/extensions.json")
    detector.robots['ignore'].append("Googlebot")


Customizing the ``Client``
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Client`` class can take an optional ``dict`` of ``request_parameters``
that contains additional parameters defined in 
https://snapsearch.io/documentation#parameters . Note that the ``url`` parameter
is always overwritten by the ``Interceptor`` with the encoded URL from the
associated ``Detector`` object. It can also take optional ``api_url`` and
``ca_path`` to communicate with an alternative backend service.


Customizing the ``Interceptor``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Interceptor`` class can take two optional callback functions, namely
``before_intercept()`` and ``after_intercept()``.

At the presence of ``before_intercept()``, the ``Interceptor`` object will
bypass any communication with the backend service of SnapSearch, and return
the ``result`` of ``before_intercept()`` as if it were returned by the
associated ``Client`` object.

.. code-block:: python

    def before_intercept(url):
        ...
        return result

As for ``after_intercept()``, the ``Interceptor`` will provide the response
from the ``Client`` object to ``after_intercept()`` which can perform, say,
data extraction or logging as appropriate.

.. code-block:: python

    def after_intercept(url, response):
        ...
        return None

The return value of ``after_response()`` is ignored by the ``Interceptor`` and
it does not affect the interception process.


Developers' Resources
=====================

- `Official Documentation of SnapSearch <https://snapsearch.io/documentation>`_
- `Future Development of the Pythonic Client Package <https://pythonhosted.org/snapsearch-client-python/develop.html>`_
