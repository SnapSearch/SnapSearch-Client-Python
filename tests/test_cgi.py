#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SnapSearch.tests.test_cgi
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests SnapSearch.cgi

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/10
"""

__all__ = ['TestControllerMethods', ]


import json
import os
import sys

try:
    from . import _config
    from ._config import unittest
except (ValueError, ImportError):
    import _config
    from _config import unittest


@unittest.skipIf(not os.environ.get('SNAPSEARCH_API_CREDENTIALS', None) and
                 os.environ.get('TRAVIS', False),
                 "API credentials are required for unsupervised testing")
class TestControllerMethods(unittest.TestCase):
    """
    Tests ``InterceptorController.__init__()`` and ``__call__()``.
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

    def test_controller_init(self):
        from SnapSearch import Interceptor
        from SnapSearch.cgi import InterceptorController
        i = Interceptor(self.client, self.detector)
        cb = lambda r: {b"status": 200,
                        b"headers": [(b"Content-Type", b"text/html"),
                                     (b"Server", b"apache (CentOS)"), ],
                        b"html": b"Hello World!\r\n", }
        ic = InterceptorController(i, cb)
        self.assertEqual(i, ic.interceptor)
        self.assertEqual(cb, ic.response_callback)
        self.assertRaises(AssertionError, ic.start)
        pass  # void return

    def test_controller_default_callback(self):
        from SnapSearch import Interceptor
        from SnapSearch.cgi import InterceptorController
        i = Interceptor(self.client, self.detector)
        ic = InterceptorController(i)
        cb = ic.response_callback
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

    def test_controller_fallback_to_normal(self):
        from SnapSearch import Interceptor
        from SnapSearch.api import response
        from SnapSearch.cgi import InterceptorController
        i = Interceptor(self.client, self.detector)

        from io import BytesIO
        old_stdout, sys.stdout = sys.stdout, BytesIO(b"Hello World!\r\n")
        ic = InterceptorController(i)
        # invalidate the ``match` list in robots, and force detector to raise
        # an exception. this will trigger the ``except`` branch in ic.__call__
        # and force it to resume to non-intercepted mode
        ic.interceptor.detector.robots['match'] = None
        environ = self.NORMAL_SITE_ENVIRON.copy()
        environ['HTTP_USER_AGENT'] = "AdsBot-Google"
        self.assertFalse(ic.start(environ))
        ic.stop(False)
        sys.stdout = old_stdout
        pass  # void return

    def test_controller_call_intercepted(self):
        from SnapSearch import Interceptor
        from SnapSearch.api import response
        from SnapSearch.cgi import InterceptorController
        i = Interceptor(self.client, self.detector)

        def cb(response_body):
            body = response._extract_message(response_body)
            self.assertTrue(isinstance(body, dict))
            self.assertTrue("html" in body)
            self.msg = body['html']
            return body

        from io import BytesIO
        old_stdout, sys.stdout = sys.stdout, BytesIO(b"Hello World!\r\n")
        ic = InterceptorController(i, cb)
        environ = self.NORMAL_SITE_ENVIRON.copy()
        environ['HTTP_USER_AGENT'] = "AdsBot-Google"
        self.assertTrue(ic.start(environ))
        self.assertTrue(self.msg.startswith(b"<html"))
        ic.stop(False)
        sys.stdout = old_stdout
        pass  # void return

    def test_controller_call_normal(self):
        from SnapSearch import Interceptor
        from SnapSearch.api import response
        from SnapSearch.cgi import InterceptorController
        i = Interceptor(self.client, self.detector)

        from io import BytesIO
        old_stdout, sys.stdout = sys.stdout, BytesIO(b"Hello World!\r\n")
        ic = InterceptorController(i)
        environ = self.NORMAL_SITE_ENVIRON.copy()
        environ['HTTP_USER_AGENT'] = "Mozilla"
        self.assertFalse(ic.start(environ))
        ic.stop(False)
        sys.stdout = old_stdout
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
