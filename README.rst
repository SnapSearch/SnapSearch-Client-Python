SnapSearch-Client-Python
========================

.. image:: http://badge.fury.io/py/SnapSearch-Client-Python.png
   :target: http://badge.fury.io/py/SnapSearch-Client-Python

.. image:: https://pypip.in/d/SnapSearch-Client-Python/badge.png?period=month
   :target: https://crate.io/packages/SnapSearch-Client-Python/
   :alt: Downloads

.. image:: https://pypip.in/license/SnapSearch-Client-Python/badge.png
   :target: https://pypi.python.org/pypi/SnapSearch-Client-Python/
   :alt: License

SnapSearch Client Python is a Python based framework agnostic HTTP client
library for SnapSearch (https://snapsearch.io/).

SnapSearch provides similar libraries in other languages:
https://github.com/SnapSearch/SnapSearch-Clients


Installation
------------

Attention: The Pythonic ``SnapSearch-Client`` is currently undergoing **alpha**
test. Consider the code base *not* suitable for use in a production system!

To install with ``pip``, simply:

.. code-block:: bash

    $ pip install SnapSearch-Client-Python

Or, if you prefer ``easy_install``:

.. code-block:: bash

    $ easy_install SnapSearch-Client-Python

The Pythonic ``SnapSearch-Client`` requires an HTTP library to verify SSL
certificates for HTTPS requests. It seamlessly supports any of PycURL_ and
requests_. You need to have one of them installled.

.. _PycURL: http://pycurl.sourceforge.net/
.. _requests: http://python-requests.org/


Usage
-----

