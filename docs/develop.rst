.. SnapSearch-Client-Python

------------------
Future Development
------------------

Overview
========

.. image:: https://travis-ci.org/liuyu81/SnapSearch-Client-Python.png?branch=master
   :target: https://travis-ci.org/liuyu81/SnapSearch-Client-Python
   :alt: Build Status

.. image:: https://pypip.in/license/SnapSearch-Client-Python/badge.png
   :target: https://pypi.python.org/pypi/SnapSearch-Client-Python/
   :alt: License

Status:
  - 3 Internal Test (Alpha)

Requires:
  - Python 2.6, 2.7, 3.2, 3.3
  - HTTP lib: PycURL_ or Requests_

.. _PycURL: http://pycurl.sourceforge.net/
.. _Requests: http://python-requests.org/


Specifications
==============

Standards
~~~~~~~~~

- :RFC:`3986` : URI
- :RFC:`3875` : CGI 1.1
- :PEP:`3333` : WSGI 1.0.1

Objects and Interfaces
~~~~~~~~~~~~~~~~~~~~~~

TODO


Design Choices
==============

TODO


Coding
======

Style Conventions
~~~~~~~~~~~~~~~~~

- :PEP:`8` -- identation and spacing
- :PEP:`287` -- comments and docstrings
- http://docs.python.org/devguide/documenting.html


Code Elements
~~~~~~~~~~~~~

String Literals:
  - key to a ``dict`` object: ``values['key']``, ``values.get('key')``
  - bytes or unicode data: ``"key" in values``
  - bytes or unicode messages: ``print("hello!")``
  - paths or file names: ``open("filename")``
  - docstring: ``"""doc"""``


Style Checking
~~~~~~~~~~~~~~~

Run the ``pep8`` tool to enforce style checking against :PEP:`8`.

.. code-block:: bash

    $ pip install pep8
    $ pep8 . --verbose


Testing
=======

Unit Test
~~~~~~~~~

The test suite of the Pythonic ``SnapSearch-Client`` is composed of ``unittest``
(``unittest2`` in Python 2.6) test cases. There are a few other tools that are
useful for style checking (``pep8``) and coverage report (``coverage``).

.. code-block:: bash

    $ pip install unittest2  # only if you are using python 2.6
    $ pip install coverage

TODO


Integration Test
~~~~~~~~~~~~~~~~

Some test cases require a set of API credentials (i.e. ``api_email`` and
``api_key``) to access the backend service of SnapSearch. When running the
test suite locally, the API credentials can be specified either as an
environment variable, i.e.,

.. code-block:: bash

    $ env SNAPSEARCH_API_CREDENTIALS=<email>:<key> \
    > coverage run --omit "*test*" -m tests -v

or typed in manually in the form of ``<email>:<key>``, i.e.,

.. code-block:: bash

    $ coverage run --omit "*test*" -m tests -v
    ...
    test_request_dynamic_page (__main__.TestClientRequest) ... API credentials: <email>:<key>
    ...

To support unsupervised testing on Travis-CI_, an encrypted message
containing this environment variable has been placed in ``.travis.yml``,

.. code-block:: yaml

    env:
      global:
        secure: "... encrypted data ..."

.. _Travis-CI: https://travis-ci.org/

For detailed instructions on how to update this encrypted message, see
http://docs.travis-ci.com/user/encryption-keys/


Profiling
~~~~~~~~~

TODO


Documentation
=============

TODO


Release
=======

TODO
