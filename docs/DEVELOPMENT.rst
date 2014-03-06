SnapSearch-Client-Python
========================

.. image:: https://travis-ci.org/liuyu81/SnapSearch-Client-Python.png?branch=master
   :target: https://travis-ci.org/liuyu81/SnapSearch-Client-Python

.. image:: http://badge.fury.io/py/SnapSearch-Client-Python.png
   :target: http://badge.fury.io/py/SnapSearch-Client-Python


Development
-----------

Status:
  - 2 Prototyping (PreAlpha)

Standards:
  - :RFC:`3986` : URI
  - :RFC:`3875` : CGI 1.1
  - :PEP:`3333` : WSGI 1.0.1

Requires:
  - Python 2.6, 2.7, 3.2, 3.3
  - HTTP lib: PycURL_ or Requests_

.. _PycURL: http://pycurl.sourceforge.net/
.. _Requests: http://python-requests.org/

Style Guide:
  - identation and spacing

    - :PEP:`8`

  - comments and docstrings

    - :PEP:`287`
    - http://docs.python.org/devguide/documenting.html

  - string literals

    - key to a ``dict`` object: ``values['key']``, ``values.get('key')``
    - bytes or unicode data: ``"key" in values``
    - bytes or unicode messages: ``print("hello!")``
    - paths or file names: ``open("filename")``
    - docstring: ``"""doc"""``

Unit Test:
    The test suite requires API credentials (i.e. ``api_email`` and
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

