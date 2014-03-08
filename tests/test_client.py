#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SnapSearch.tests.test_client
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests SnapSearch.client

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['TestClientInit',
           'TestClientMethods', ]


import os
import sys

try:
    from . import _config
    from ._config import unittest
except (ValueError, ImportError):
    import _config
    from _config import unittest


class TestClientInit(unittest.TestCase):
    """
    Tests different ways to initialize a Client object.
    """

    @classmethod
    def setUpClass(cls):
        cls.api_email = "fantasy@email.com"
        cls.api_key = "fantasy_Api_Key"
        cls.HTTPS_API = "https://snapsearch.io/api/v1/robot"
        cls.NON_HTTPS_API = "http://snapsearch.io/api/v1/robot"
        cls.EXTERNAL_CA_BUNDLE_PEM = _config.save_temp(
            "cacert.pem", _config.DATA_CA_BUNDLE_PEM.encode("utf-8"))
        cls.NON_EXISTENT_PEM = _config.save_temp(
            "no_such_file", b"") + ".pem"
        pass  # void return

    def test_client_init(self):
        # initialize with default arguments
        from SnapSearch import Client
        client = Client(self.api_email, self.api_key, {'test': 1})
        pass  # void return

    def test_client_init_external_api_url(self):
        # initialize with default arguments
        from SnapSearch import Client, error
        # https api url
        client = Client(
            self.api_email, self.api_key, {'test': 1}, api_url=self.HTTPS_API)
        # non-https api url
        self.assertRaises(
            error.SnapSearchError, Client, self.api_email, self.api_key,
            {'test': 1}, api_url=self.NON_HTTPS_API)
        pass  # void return

    def test_client_init_external_ca_path(self):
        from SnapSearch import Client, error
        # existing pem file
        client = Client(
            self.api_email, self.api_key, ca_path=self.EXTERNAL_CA_BUNDLE_PEM)
        # non-existent pem file
        self.assertRaises(
            error.SnapSearchError, Client, self.api_email, self.api_key,
            {'test': 1}, ca_path=self.NON_EXISTENT_PEM)
        pass  # void return

    pass


@unittest.skipIf(not os.environ.get('SNAPSEARCH_API_CREDENTIALS', None) and
                 os.environ.get('TRAVIS', False),
                 "API credentials are required for unsupervised testing")
class TestClientMethods(unittest.TestCase):
    """
    Test ``Client.__call__()`` with different URL's.
    """

    @classmethod
    def setUpClass(cls):
        cls.BAD_API_URL = "https://non.existent/site"
        cls.NORMAL_SITE_URL = "https://snapsearch.io/"
        cls.INVALID_SITE_URL = "email:liuyu@opencps.net"
        cls.NON_EXISTENT_SITE_URL = "https://www.google.com/non-existent"
        cls.api_email, cls.api_key = _config.get_api_credentials()
        pass  # void return

    def test_client_call_bad_api_url(self):
        from SnapSearch import Client, error
        client = Client(
            self.api_email, self.api_key, {'test': 1},
            api_url=self.BAD_API_URL)
        self.assertRaises(error.SnapSearchConnectionError, client,
                          self.NORMAL_SITE_URL)
        pass  # void return

    def test_client_call_normal_site_url(self):
        from SnapSearch import Client
        client = Client(self.api_email, self.api_key, {'test': 1})
        response = client(self.NORMAL_SITE_URL)
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(response.get('status', None), 200)
        pass  # void return

    def test_client_call_missing_site_url(self):
        from SnapSearch import Client
        client = Client(self.api_email, self.api_key, {'test': 1})
        response = client(self.NON_EXISTENT_SITE_URL)
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(response.get('status', None), 404)
        pass  # void return

    def test_client_call_validation_error(self):
        from SnapSearch import Client, error
        client = Client(self.api_email, self.api_key, {'test': 1})
        self.assertRaises(error.SnapSearchError, client, self.INVALID_SITE_URL)
        pass  # void return

    def test_client_call_bad_response(self):
        # uses a dummy dispatch function to emulate a broken backend service
        # returning None as response, causing client.__call__() to raise error.
        from SnapSearch import Client, error
        client = Client(self.api_email, self.api_key, {'test': 1})

        def dummy_dispatch(**kwds):
            return None

        from SnapSearch import api
        old_dispatch = api.dispatch
        api.dispatch = dummy_dispatch
        self.assertRaises(error.SnapSearchError, client, self.NORMAL_SITE_URL)
        api.dispatch = old_dispatch
        pass  # void return

    def test_client_call_unknown_response(self):
        # uses a dummy dispatch function to emulate a broken backend service
        # returning unknown response code, causing client.__call__() to fail.
        from SnapSearch import Client
        from SnapSearch.api.response import Response
        client = Client(self.api_email, self.api_key, {'test': 1})

        def dummy_dispatch(**kwds):
            return Response(status=200, headers=[(), ()],
                            body={'code': "unknown", 'content': "unknown"})

        from SnapSearch import api
        old_dispatch = api.dispatch
        api.dispatch = dummy_dispatch
        response = client(self.NORMAL_SITE_URL)
        self.assertEqual(response, None)
        api.dispatch = old_dispatch
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
