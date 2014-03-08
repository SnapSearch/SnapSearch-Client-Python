==================================
Integration with WSGI Applications
==================================
------------------------------------------------------
Interceptor Middleware from Pythonic SnapSearch Client
------------------------------------------------------

Overview
========

The `Pythnoic SnapSearch Client`__ comes with a `WSGI`_-compliant Interceptor
Middleware for easy integration with existing web applications. The solution is
framework agnostic, and supports any `WSGI`_-compliant web applications, either
hand-made, or built upon `WSGI`_ framewrorks (such as Django_, Falcon_, Flask_,
web2py_, etc.).

.. __: https://github.com/liuyu81/SnapSearch-Client-Python/
.. _WSGI: http://legacy.python.org/dev/peps/pep-3333/
.. _Django: https://www.djangoproject.com/
.. _Falcon: http://falconframework.org
.. _Flask: http://flask.pocoo.org/
.. _web2py: http://web2py.com/


Flask App
=========

.. code:: python

    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        return "Hello World!\r\n"

    if __name__ == '__main__':
        app.run(host="0.0.0.0", port=5000)


Interception
============
