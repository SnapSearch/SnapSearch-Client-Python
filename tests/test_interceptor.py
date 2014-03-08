#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SnapSearch.tests.test_interceptor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests SnapSearch.interceptor

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['TestInterceptorMethods', ]


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
class TestInterceptorMethods(unittest.TestCase):
    """
    Tests ``Interceptor.__init__()`` and ``Interceptor.__call__()``.
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
        cls.NORMAL_SITE_ENVIRON = {
            'HTTP_USER_AGENT': "AdsBot-Google",
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

    def test_interceptor_init(self):
        from SnapSearch import Interceptor
        i = Interceptor(self.client, self.detector)
        self.assertEqual(i.client, self.client)
        self.assertEqual(i.detector, self.detector)
        pass  # void return

    def test_interceptor_call_no_intercept(self):
        from SnapSearch import Interceptor
        i = Interceptor(self.client, self.detector)
        response = i(self.FIREFOX_REQUEST)
        self.assertEqual(response, None)
        pass  # void return

    def test_interceptor_call_with_intercept(self):
        from SnapSearch import Interceptor
        i = Interceptor(self.client, self.detector)
        response = i(self.NORMAL_SITE_ENVIRON)
        self.assertTrue(isinstance(response, dict))
        self.assertTrue("status" in response)
        self.assertTrue(response["status"])  # may not be 200
        pass  # void return

    def test_interceptor_init_callback(self):
        from SnapSearch import Interceptor
        cb_pre = lambda url: None
        cb_post = lambda url, resp: None
        i = Interceptor(self.client, self.detector, cb_pre, cb_post)
        self.assertEqual(i.before_intercept, cb_pre)
        self.assertEqual(i.after_intercept, cb_post)
        pass  # void return

    def test_interceptor_pre_callback(self):
        # pre-intercaption callback
        from SnapSearch import Interceptor
        cb_pre = lambda url: {'url': url}
        i = Interceptor(self.client, self.detector, cb_pre)
        response = i(self.NORMAL_SITE_ENVIRON)
        self.assertTrue(isinstance(response, dict))
        self.assertTrue("url" in response)
        self.assertEqual(response['url'], self.NORMAL_SITE_URL)
        pass  # void return

    def test_interceptor_post_callback(self):
        # post-intercaption callback
        from SnapSearch import Interceptor

        def cb_post(url, response):
            response['status'] = -1
            return None

        i = Interceptor(self.client, self.detector, None, cb_post)
        response = i(self.NORMAL_SITE_ENVIRON)
        self.assertEqual(response['status'], -1)
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
