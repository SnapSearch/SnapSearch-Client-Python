.. snapsearch-client-python document
   :noindex:

------------------
Future Development
------------------

Overview
========

.. image:: https://travis-ci.org/SnapSearch/SnapSearch-Client-Python.png?branch=master
   :target: https://travis-ci.org/SnapSearch/SnapSearch-Client-python
   :alt: Build Status

.. image:: https://pypip.in/license/snapsearch-client-python/badge.png
   :target: https://pypi.python.org/pypi/snapsearch-client-python/
   :alt: License

Status:
  - 4 Public Test (Beta)

Requires:
  - Python 2.6, 2.7, 3.2, 3.3
  - HTTP library: PycURL_ or Requests_

.. _PycURL: http://pycurl.sourceforge.net/
.. _Requests: http://python-requests.org/


Specifications
==============

Standards
~~~~~~~~~

- :RFC:`2616` : HTTP 1.1
- :RFC:`3875` : CGI 1.1
- :PEP:`3333` : WSGI 1.0.1

Data Exchange Formats
~~~~~~~~~~~~~~~~~~~~~

- :RFC:`3986` : URI
- `ECMA 404 <http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-404.pdf>`_: JSON
- Google AJAX crawling: https://developers.google.com/webmasters/ajax-crawling/docs/specification
- SnapSearch backend service: https://snapsearch.io/documentation#apiUsage

Modules, Objects and Interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The code base of the `Pythonic SnapSearch Client`_ consists of four functional
bundles of files, namely,

.. _`Pythonic SnapSearch Client`: https://github.com/SnapSearch/SnapSearch-Client-Python

1. main package: ``src/SnapSearch``.
2. test suite: ``tests/`` and ``.travis.yml``.
3. documentation: ``docs/``, ``examples/``, ``LICENSE``, and ``README.rst``.
4. distribution: ``MANIFEST.in`` and ``setup.py``.

The main package exhibits three layers of abstraction, namely,

1. backend service layer (``SnapSearch.api``): interfaces, parameters, and
   resource bundles for communication and data exchange with the backend service.
2. core objects layer (``SnapSearch.Client``, ``SnapSearch.Detector``,
   ``SnapSearch.Interceptor``, and ``SnapSearch.error``): framework agnostic
   objects and interfaces for advanced users of the client package.
3. application bindings layer (i.e. ``SnapSearch.cgi`` and ``SnapSearch.wsgi``):
   compositions and extensions of the core objects to simplify the integration
   of the client package with Python web applications.

The core objects are not unique to the `Pythonic SnapSearch Client`_, the
naming, functionality and interoperability of these objects are ubiquitious
among all client packages of SnapSearch.

Coding Style Conventions
~~~~~~~~~~~~~~~~~~~~~~~~

- :PEP:`8` -- identation and spacing
- :PEP:`287` -- comments and docstrings
- http://docs.python.org/devguide/documenting.html

Design Choices
==============

To enable the integration of SnapSearch into mainstream Python Web technologies,
and to accommodate potential, future changes in SnapSearch's backend service,
we have made a number of design choices when implementating the Pythonic client
package. This section explains the rationale behind these design choices.

Stateless Core Objects
~~~~~~~~~~~~~~~~~~~~~~

The Pythonic client package decouples the three core objects, aka. ``Client``,
``Detector``, and ``Interceptor``, from the incoming HTTP request. Specifically,
the construction / instantiation of these three objects do NOT depend on
information from a particular HTTP request. Moreover, instances of these three
objects do NOT keep any internal states binding to an HTTP request.

Taking the ``Detector`` object for example, the only chance an instance of
``Detector`` ever sees an incoming HTTP request is through its ``__call__()``
method. The return value of this ``__call__()`` method is an encoded URL in
case the request is eligible for interception with SnapSearch, or ``None``
otherwise.

.. code-block:: python

    class Detector(object):
        def __init__(self, ...):
            ...
        def __call__(self, request):
            """__call__(request) -> url or None"""

The benefit of having a stateless ``Detector`` is that, when serving multiple
(and possibly concurrent) HTTP requests within a long-running server process --
as is the case of WSGI web applications -- all the detection tasks can be
performed with a singleton ``Detector`` object. And the overhead of initializing
the ``Detector`` object does *not* add to the response time serving each
incoming HTTP request.


Backend Service Abstraction Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Pythonic client package wraps the communication and data exchange with the
backend service of SnapSearch in the ``SnapSearch.api`` subpackage, which forms
an abstraction layer for the backend service.

This abstraction layer collects data conversion methods, protocols, parameters,
and resource bundles, that are essential for invoking the backend service, yet
do not need to be exposed to users of the client package.

Two pinciples were followed when designing this *backend service abstraction
layer*.

1. encapsulation of details: such that if the backend service ever changes, the
   change should be contained within the ``api`` subpackage. Namely, the core
   objects and the application bindings layers should be able to remain intact.
2. preservation of information: such that if users of the client package ever
   need a piece of information available in the raw response from the backend
   service, they do *not* need to dig into the implimentation details of the
   ``api`` subpackage.


Message Extraction Decorator(s)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An intersting example practising the two design principles of the *backend
service abstraction layer* (aka. ``SnapSearch.api``) is the message extraction
decorator defined in ``api.response``.

The ``wsgi.InterceptorMiddleware`` and ``cgi.InterceptorController`` objects
from the application bindings layer are for integrating SnapSearch with
respective web applications. When the incoming HTTP request is eligible for
interception (i.e. coming from a search engine robot), these two objects will
send out search-engine-optimized responses from the backend service of
SnapSearch. The customizable ``response_callback`` functions of respective
objects are responsible for converting JSON-deserialized data structure from
the backend service into valid HTTP messages (containing status code, headers,
and html content).

For users *not* knowing the details structure of the backend's response body,
the ``api`` subpackage provides a pre-processing decorator that extracts and
converts the response body into a simple ``dict`` of the form,

.. code-block:: json

    {
        "code": 200,
        "headers":
        [
            ["Content-Type", "html"],
            ["Date", "Thu, 13 Mar 2014 14:20:18 GMT"]
        ],
        "html": "<html><head> ... </html>"
    }

And the implementation of a ``response_callback`` becomes straightforward,

.. code-block:: python

    import SnapSearch.api as api
    @api.response.message_extractor
    def response_callback(response_body):
        """Removes all HTTP headers except Location"""
        response_body['headers'] = [
            (key, val) for key, val in response_body['headers']
            if key.lower() in (b"location", )]
        return response_body

For advanced users that *do* need to manipulate the raw response body. They can
simply remove the decorator and receive the full response body as defined in
https://snapsearch.io/documentation#parameters

Test Suite
==========

Style Checking
~~~~~~~~~~~~~~

The preliminary form of testing is to run the ``pep8`` tool over the source code
to enforce style conformance to :PEP:`8`.

.. code-block:: bash

    $ pip install pep8
    $ pep8 . --verbose


Unit Test
~~~~~~~~~

The test suite of the Pythonic ``SnapSearch-Client`` is composed of ``unittest``
(``unittest2`` in Python 2.6) test cases. They can be executed either directly
as runnable python modules, i.e.,

.. code-block:: bash

    $ pip install unittest2  # only if you are using python 2.6
    $ python -m tests.test_detector -v

Or, invoked by third-party testing tools, such as ``coverage``.

.. code-block:: bash

    $ pip install coverage
    $ coverage run -m tests.test_detector -v

API Credentials
~~~~~~~~~~~~~~~

Some test cases require API credentials (i.e. ``api_email`` and ``api_key``) to
access the backend service of SnapSearch. When running these test cases, there
will be a prompt asking for the credentials in the form of ``<email>:<key>``,

.. code-block:: bash

    $ coverage run -m tests.test_client -v
    test_client_init (__main__.TestClientInit) ... ok
    test_client_init_external_api_url (__main__.TestClientInit) ... ok
    test_client_init_external_ca_path (__main__.TestClientInit) ... ok
    test_client_call_bad_api_url (__main__.TestClientMethods) ... ok
    API credentials: <email>:<key>
    ...

The API credentials can also be specified as an environment variable, i.e.,

.. code-block:: bash

    $ env SNAPSEARCH_API_CREDENTIALS=<email>:<key> \
    > coverage run -m tests -v

Integration Test
~~~~~~~~~~~~~~~~

Besides running test cases locally, the source code repository also enforces
unsupervised integration test through Travis-CI_. The setup script for
integration test is ``.travis.yml``.

To make API credentials available to unsupervised integration test, the
environment variable ``SNAPSEARCH_API_CREDENTIALS`` is kept in ``.travis.yml``
as encrypted data.

.. code-block:: yaml

    env:
      global:
        secure: "... encrypted data ..."

.. _Travis-CI: https://travis-ci.org/

For detailed instructions on how to update this encrypted data, see
http://docs.travis-ci.com/user/encryption-keys/


Test Coverage
~~~~~~~~~~~~~

When revisions have been committed to the code base, it is important to ensure
those new changes are covered by test cases. It would help to review the test
coverage statistics after each ``coverage run``, i.e.,

.. code-block:: bash

    $ env SNAPSEARCH_API_CREDENTIALS=<email>:<key> \
    > coverage run --omit ""*test*,*requests*,*curl*,*pkg*"" -m tests -v
    $ coverage report -m
    Name                          Stmts   Miss  Cover   Missing
    -----------------------------------------------------------
    src/SnapSearch/__init__          11      0   100%   
    src/SnapSearch/_compat           30     10    67%   37-43, 52-53, 69, 79
    src/SnapSearch/api/__init__      22      0   100%   
    src/SnapSearch/api/backend       83     20    76%   46-73, 144-145, 153, 166-168, 175-176, 186
    src/SnapSearch/api/environ       59      0   100%   
    src/SnapSearch/api/response      49      0   100%   
    src/SnapSearch/cgi               57      0   100%   
    src/SnapSearch/client            36      0   100%   
    src/SnapSearch/detector          77      0   100%   
    src/SnapSearch/error             15      0   100%   
    src/SnapSearch/interceptor       34      0   100%   
    src/SnapSearch/wsgi              35      0   100%   
    -----------------------------------------------------------
    TOTAL                           508     30    94%   

In case there are missing lines for modules other than ``_compat`` and
``api.backend`` (these two modules handle compatibility issues across different
platforms, so the low test coverage is expected), there should be a new test
case to improve the coverage.


Release
=======

Release the source tarball to `PyPI`_ -- the official Python packages index.
Remember to bump the version number (or delete any previous release having the
same version number).

.. _`PyPI`: https://pypi.python.org

.. code-block:: bash

    $ python setup.py sdist upload

For further information about distributing Python modules, see
http://docs.python.org/distutils/
