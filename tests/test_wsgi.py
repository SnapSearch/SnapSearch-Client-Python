#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SnapSearch.tests.test_wsgi
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests SnapSearch.wsgi

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['TestMiddlewareMethods', ]


import json
import os
import sys

try:
    from . import _config
    from ._config import unittest
except (ValueError, ImportError):
    import _config
    from _config import unittest


class DummyApp(object):
    """
    Dummy WSGI application
    """
    def __call__(self, environ, start_response):
        start_response(b"200 OK", [(b"Content-Type", b"text/html"), ])
        return b"Hello World!\r\n"

    pass


@unittest.skipIf(not os.environ.get('SNAPSEARCH_API_CREDENTIALS', None) and
                 os.environ.get('TRAVIS', False),
                 "API credentials are required for unsupervised testing")
class TestMiddlewareMethods(unittest.TestCase):
    """
    Tests ``InterceptorMiddleware.__init__()`` and ``__call__()``.
    """

    @classmethod
    def setUpClass(cls):
        from SnapSearch import Client, Detector
        cls.api_email, cls.api_key = _config.get_api_credentials()
        cls.client = Client(cls.api_email, cls.api_key, {'test': 1})
        cls.detector = Detector()
        cls.ADSBOT_GOOG_GET = json.loads(_config.DATA_ADSBOT_GOOG_GET)
        cls.FIREFOX_REQUEST = json.loads(_config.DATA_FIREFOX_REQUEST)
        cls.NORMAL_SITE_URL = "http://snapsearch.io/"
        pass  # void return

    def setUp(self):
        self.NORMAL_SITE_ENVIRON = {
            'SERVER_NAME': "snapsearch.io",
            'SERVER_PORT': "80",
            'SCRIPT_NAME': "/",
            'PATH_INFO': "",
            'REQUEST_METHOD': "GET",
            'SERVER_PROTOCOL': "HTTP/1.1",
            'QUERY_STRING': "",
            'GATEWAY_INTERFACE': "CGI/1.1",
            'HTTPS': "off", }
        pass  # void return

    def test_middleware_init(self):
        from SnapSearch import Interceptor
        from SnapSearch.wsgi import InterceptorMiddleware
        a = DummyApp()
        i = Interceptor(self.client, self.detector)
        cb = lambda r: {b"status": 200,
                        b"headers": [(b"Content-Type", b"text/html"),
                                     (b"Server", b"apache (CentOS)"), ],
                        b"html": b"Hello World!\r\n", }
        im = InterceptorMiddleware(a, i, cb)
        self.assertEqual(a, im.application)
        self.assertEqual(i, im.interceptor)
        self.assertEqual(cb, im.response_callback)
        pass  # void return

    def test_middleware_default_callback(self):
        from SnapSearch import Interceptor
        from SnapSearch.wsgi import InterceptorMiddleware
        a = DummyApp()
        i = Interceptor(self.client, self.detector)
        im = InterceptorMiddleware(a, i)
        cb = im.response_callback
        self.assertTrue(callable(cb))
        # bad response with dirty headers
        response = {'status': 200,
                    'headers': [('name', 'value'),  # not a dict
                                {'name': 1, },  # no value
                                {'value': 1, },  # no name
                                {}, ],
                    'html': ""}
        message = cb(response)
        self.assertTrue(isinstance(message, dict))
        self.assertTrue("headers" in message)
        pass  # void return

    def test_middleware_fallback_to_normal(self):
        from SnapSearch import Interceptor
        from SnapSearch.wsgi import InterceptorMiddleware
        a = DummyApp()
        i = Interceptor(self.client, self.detector)
        im = InterceptorMiddleware(a, i)

        def start_response(status, headers, exc_info=None):
            self.assertEqual(status, b"200 OK")
            self.assertTrue(headers)

        # invalidaate the ``match` list in robots, and force detector to raise
        # an exception. this will trigger the ``except`` branch in im.__call__
        # and force it to resume to non-intercepted mode
        im.interceptor.detector.robots['match'] = None
        environ = self.NORMAL_SITE_ENVIRON.copy()
        environ['HTTP_USER_AGENT'] = "AdsBot-Google"
        msg = im(environ, start_response)
        self.assertTrue(msg.startswith(b"Hello"))
        pass  # void return

    def test_middleware_call_intercepted(self):
        from SnapSearch import Interceptor
        from SnapSearch.wsgi import InterceptorMiddleware
        a = DummyApp()
        i = Interceptor(self.client, self.detector)
        im = InterceptorMiddleware(a, i)

        def start_response(status, headers, exc_info=None):
            self.assertTrue(status)  # may not be b"200 OK"
            self.assertTrue(headers)

        environ = self.NORMAL_SITE_ENVIRON.copy()
        environ['HTTP_USER_AGENT'] = "AdsBot-Google"
        msg = im(environ, start_response)
        self.assertTrue(msg.startswith(b"<html"))
        pass  # void return

    def test_middleware_call_normal(self):
        from SnapSearch import Interceptor
        from SnapSearch.wsgi import InterceptorMiddleware
        a = DummyApp()
        i = Interceptor(self.client, self.detector)
        im = InterceptorMiddleware(a, i)

        def start_response(status, headers, exc_info=None):
            self.assertEqual(status, b"200 OK")
            self.assertTrue(headers)

        environ = self.NORMAL_SITE_ENVIRON.copy()
        environ['HTTP_USER_AGENT'] = "Mozilla"
        msg = im(environ, start_response)
        self.assertTrue(msg.startswith(b"Hello"))
        pass  # void return

    pass


def test_suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(eval(c)) for c in __all__])


if __name__ == '__main__':
    # local SnapSearch package takes precedence
    sys.path.insert(0, os.path.join(os.path.curdir, "..", "src"))
    sys.path.insert(0, os.path.join(os.path.curdir, ".."))
    sys.path.insert(0, os.path.join(os.path.curdir, "src"))
    sys.path.insert(0, os.path.join(os.path.curdir))
    unittest.main(defaultTest='test_suite')
