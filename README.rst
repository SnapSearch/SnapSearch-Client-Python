SnapSearch-Client-Python
========================

.. image:: https://travis-ci.org/liuyu81/SnapSearch-Client-Python.png?branch=master
	:target: https://travis-ci.org/liuyu81/SnapSearch-Client-Python

.. image:: http://badge.fury.io/py/SnapSearch-Client-Python.png
	:target: http://badge.fury.io/py/SnapSearch-Client-Python

Snapsearch Client Python is Python based framework agnostic HTTP client library for SnapSearch (https://snapsearch.io/).

SnapSearch provides similar libraries in other languages: https://github.com/SnapSearch/SnapSearch-Clients


Development
------------------

Status:
  - 2 Prototyping (PreAlpha)

Standards:
  - :RFC:`3986` : URI
  - :RFC:`3875` : CGI 1.1
  - :PEP:`3333` : WSGI 1.0.1

Style Guide:
  - :PEP:`8` : identation and spacing
  - :PEP:`287` : comments and docstrings
  - string literals

    - key to a ``dict`` object: ``values['key']``, ``values.get('key')``
    - bytes or unicode data: ``"key" in values``
    - bytes or unicode messages: ``print("hello!")``
    - paths or file names: ``open("filename")``
    - docstring: ``"""doc"""``

Requires:
  - Python 2.6, 2.7, 3.2, 3.3
  - HTTP lib: PycURL_ or Requests_

.. _PycURL: http://pycurl.sourceforge.net/
.. _Requests: http://python-requests.org/


Installation
------------

To install with pip, simply:

.. code-block:: bash

    $ pip install SnapSearch-Client-Python

Or, if you prefer easy_install:

.. code-block:: bash

    $ easy_install SnapSearch-Client-Python


Usage
-----
