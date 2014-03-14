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

.. _`Pythonic SnapSearch Client`: https://github.com/SnapSearch/
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

1. server servers the CGI script at ``http://<server_ip>:5000/``.

.. code-block:: none

    # Apache server's virtual host configuration (partial)
    <VirtualHost *:5000>
        ServerName <server_name>
        CustomLog /<server_root>/log/access
        ...
        DocumentRoot /<server_root>/cgi/
        ScriptAlias /cgi/ /<server_root>/cgi/
        <Directory /<server_root>/cgi>
            Options +ExecCGI
            SetHandler cgi-script
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
    <robot_ip> - - [13/Mar/2014:22:20:19 +0800] "GET /main.py HTTP/1.1" 200 14
    <snapsearch_ip> - - [13/Mar/2014:22:20:18 +0800] "GET /main.py HTTP/1.1" 200 107
