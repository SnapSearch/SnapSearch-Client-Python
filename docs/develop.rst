.. snapsearch-client-python document
   :noindex:

------------------
Future Development
------------------

Overview
========

.. image:: https://travis-ci.org/liuyu81/SnapSearch-Client-Python.png?branch=master
   :target: https://travis-ci.org/liuyu81/SnapSearch-Client-python
   :alt: Build Status

.. image:: https://pypip.in/license/snapsearch-client-python/badge.png
   :target: https://pypi.python.org/pypi/snapsearch-client-python/
   :alt: License

Status:
  - 3 Internal Test (Alpha)

Requires:
  - Python 2.6, 2.7, 3.2, 3.3
  - HTTP library: PycURL_ or Requests_

.. _PycURL: http://pycurl.sourceforge.net/
.. _Requests: http://python-requests.org/


Specifications
==============

Standards
~~~~~~~~~

- :RFC:`3986` : URI
- :RFC:`3875` : CGI 1.1
- :PEP:`3333` : WSGI 1.0.1

Packages, Objects and Interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO

Source Code Repository
~~~~~~~~~~~~~~~~~~~~~~

The code base of the `Pythonic SnapSearch Client`_ consists of four bundles of files, 
namely,

.. _`Pythonic SnapSearch Client`: https://github.com/SnapSearch/SnapSearch-Client-Python

1. main package: ``src/SnapSearch``.
2. test suite: ``tests/`` and ``.travis.yml``.
3. documentation: ``docs/``, ``examples/``, ``LICENSE``, and ``README.rst``.
4. miscellaneous: ``MANIFEST.in`` and ``setup.py``.


Coding Style Conventions
~~~~~~~~~~~~~~~~~~~~~~~~

- :PEP:`8` -- identation and spacing
- :PEP:`287` -- comments and docstrings
- http://docs.python.org/devguide/documenting.html

Design Choices
==============

To enable the integration of SnapSearch into mainstream Python Web technologies, we
have made a number of design choices when implementating the Pythonic client package.
This section explains the rationale behind these design choices.

Stateless Core Objects
~~~~~~~~~~~~~~~~~~~~~~

The Pythonic client package decouples the three core objects, aka. ``Client``,
``Detector``, and ``Interceptor`` from the incoming HTTP request. In particular,
the construction of any of these three objects should be isolated from an HTTP
request object. Moreover, there cannot be any internal states binding an instance
of any of these three objects with a specific HTTP request.

Taking the ``Detector`` for example,


Backend Service Abstraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Pythonic client package emplo
    
TODO

Data Processing Responsibilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO


Test Suite
==========

The test suite of the Pythonic ``SnapSearch-Client`` is composed of ``unittest``
(``unittest2`` in Python 2.6) test cases. The test cases can be executed either
directly as runnable python modules, or invoked by third-party test tools such
as ``coverage``.

Style Checking
~~~~~~~~~~~~~~

The preliminary form of testing is to run the ``pep8`` tool over the source code
to enforce style conformance to :PEP:`8`.

.. code-block:: bash

    $ pip install pep8
    $ pep8 . --verbose


Unit Test
~~~~~~~~~

There are a few other tools that are useful for style checking (``pep8``) and coverage report (``coverage``).

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


Release
=======

Release the source tarball to `PyPI`_ -- the official Python packages index.
Remember to bump the version number (or delete the previous release having the
same version number).

.. _`PyPI`: https://pypi.python.org

.. code-block:: bash

    $ python setup.py sdist upload
