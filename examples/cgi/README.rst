.. snapsearch-client-python document
   :noindex:


Integration with Python CGI Scripts
===================================

Overview
--------

The `Pythonic SnapSearch Client`_ comes with a `CGI`_-compliant Interceptor
Controller for easy integration with existing Python CGI scripts. Note that,
this article focuses on how to glue a *Python* CGI script with the `Pythonic
SnapSearch Client`_. For intercepting `CGI`_ programs written in a different
programming language, please refer to other variations of `SnapSearch Client
<https://github.com/SnapSearch/SnapSearch-Clients>`_.

.. _`Pythonic SnapSearch Client`: https://github.com/liuyu81/
    SnapSearch-Client-Python/
.. _`CGI`: http://docs.python.org/library/cgi.html


CGI Script
----------

.. code-block:: python

    #!/usr/bin/env python

    import cgi
    import cgitb
    import sys

    def hello_world():
        msg = b"Hello World!"
        sys.stdout.write(b"Status: 200 OK\r\n")
        sys.stdout.write(b"Content-Type: text/html; charset=utf-8\r\n")
        sys.stdout.write(b"Content-Length: ")
        sys.stdout.write(bytes(len(msg)))
        sys.stdout.write(b"\r\n\r\n")
        sys.stdout.write(msg)
        sys.stdout.write(b"\r\n")
        return 0

    if __name__ == '__main__':
        sys.exit(hello_world())


Integration
-----------

1. initialize an ``Interceptor``.

.. code-block:: python

    from SnapSearch import Client, Detector, Interceptor
    interceptor = Interceptor(Client(api_email, api_key), Detector())


2. deploy the ``Interceptor``.

.. code-block:: python

    from SnapSearch.cgi import InterceptorController
    InterceptorController(interceptor).start()


3. putting it all together.

.. code-block:: python

    #!/usr/bin/env python

    import cgi
    import sys

    def hello_world():
        msg = b"Hello World!"
        sys.stdout.write(b"Status: 200 OK\r\n")
        sys.stdout.write(b"Content-Type: text/html; charset=utf-8\r\n")
        sys.stdout.write(b"Content-Length: ")
        sys.stdout.write(bytes(len(msg)))
        sys.stdout.write(b"\r\n\r\n")
        sys.stdout.write(msg)
        sys.stdout.write(b"\r\n")
        return 0

    if __name__ == '__main__':
        # API credentials
        api_email = "<email>"  # change this to the registered email
        api_key = "<key>"  # change this to the real api credential

        # initialize the interceptor
        from SnapSearch import Client, Detector, Interceptor
        interceptor = Interceptor(Client(api_email, api_key), Detector())

        # deploy the interceptor
        from SnapSearch.cgi import InterceptorController
        InterceptorController(interceptor).start()

        # start servicing
        sys.exit(hello_world())


Verification
------------

TODO
