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


Flask App
---------

Flask_ is a `WSGI`_ compliant microframework for web applications. The following
Python script serves a simple ``"Hello World"`` page through any of the public
IP address(es) of the runner machine.

.. code:: python

    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return "Hello World!\r\n"

    if __name__ == '__main__':
        app.run(host="0.0.0.0", port=5000)


Integration
-----------

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


Verification
------------

1. server starts the web application.

.. code-block:: bash

    $ pip install Flask
    $ pip install snapsearch-client-python
    $ python main.py
     * Running on http://0.0.0.0:5000/

2. search engine robot visits (emulated with ``curl``),

.. code-block:: bash

    $ curl -i -A "Googlebot" http://<server_ip>:5000/

and receives an *intercepted* HTTP response.

.. code-block:: none

    HTTP/1.0 200 OK
    server: Werkzeug/0.9.4 Python/2.6.6
    Connection: close
    Date: Wed, 12 Mar 2014 16:48:25 GMT

    <html><head><style type="text/css">body { background: #fff }</style></head><body>Hello World!
    </body></html>

3. server log shows both the robot and SnapSearch backend service.

.. code-block:: none

     * Running on http://0.0.0.0:5000/
    <robot_ip> - - [13/Mar/2014 00:42:59] "GET / HTTP/1.1" 200 -
    <snapsearch_ip> - - [13/Mar/2014 00:46:21] "GET / HTTP/1.1" 200 -
