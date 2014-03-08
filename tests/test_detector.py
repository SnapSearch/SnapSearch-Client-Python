#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SnapSearch.tests.test_detector
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests SnapSearch.detector

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

# future import should come first
from __future__ import with_statement

__all__ = ['TestDetectorInit',
           'TestDetectorMethods',
           'TestDetectorProperties', ]


import os
import sys

try:
    from . import _config
    from ._config import json, unittest
except (ValueError, ImportError):
    import _config
    from _config import json, unittest


class TestDetectorInit(unittest.TestCase):
    """
    Tests ``Detector.__init__()`` with different parameter combinations.
    """

    @classmethod
    def setUpClass(cls):
        # save local data to temporary files
        cls.EXTERNAL_ROBOTS_JSON = _config.save_temp(
            "robots.json", _config.DATA_ROBOTS_JSON.encode("utf-8"))
        cls.EXTERNAL_EXTENSIONS_JSON = _config.save_temp(
            "extensions.json", _config.DATA_EXTENSIONS_JSON.encode("utf-8"))
        cls.NON_EXISTENT_JSON = _config.save_temp(
            "no_such_file", b"") + ".json"
        pass  # void return

    def test_detector_init(self):
        # initialize with default arguments
        from SnapSearch import Detector
        detector = Detector()
        # make sure the default `robots.json` is loaded
        self.assertTrue(hasattr(detector, 'robots'))
        self.assertTrue(detector.robots)
        self.assertTrue("Bingbot" in detector.robots['match'])
        # make sure the default `extensions.json` is loaded
        self.assertTrue(hasattr(detector, 'extensions'))
        self.assertTrue(detector.extensions)
        self.assertTrue("html" in detector.extensions['generic'])
        pass  # void return

    def test_detector_init_external_robots_json(self):
        # initialize with external `robots.json`
        from SnapSearch import Detector
        detector = Detector(robots_json=self.EXTERNAL_ROBOTS_JSON)
        self.assertTrue(detector.robots)
        self.assertTrue("Testbot" in detector.robots['match'])
        # non-existent json file
        self.assertRaises(
            IOError, Detector, robots_json=self.NON_EXISTENT_JSON)
        pass  # void return

    def test_detector_init_external_extensions_json(self):
        # initialize with external `extensions.json`
        from SnapSearch import Detector
        detector = Detector(
            check_file_extensions=True,
            extensions_json=self.EXTERNAL_EXTENSIONS_JSON)
        self.assertTrue(detector.extensions)
        self.assertTrue("test" in detector.extensions['generic'])
        # specified `extensions.json` but `check_file_extensions` is False
        self.assertRaises(
            AssertionError, Detector, check_file_extensions=False,
            extensions_json=self.EXTERNAL_EXTENSIONS_JSON)
        # non-existent json file
        self.assertRaises(
            IOError, Detector, check_file_extensions=True,
            extensions_json=self.NON_EXISTENT_JSON)
        pass  # void return

    pass


class TestDetectorMethods(unittest.TestCase):
    """
    Test ``Detector.__call__()`` with different requests.
    """

    @classmethod
    def setUpClass(cls):
        cls.FIREFOX_REQUEST = json.loads(_config.DATA_FIREFOX_REQUEST)
        cls.SAFARI_REQUEST = json.loads(_config.DATA_SAFARI_REQUEST)
        cls.ADSBOT_GOOG_GET = json.loads(_config.DATA_ADSBOT_GOOG_GET)
        cls.ADSBOT_GOOG_HTML = json.loads(_config.DATA_ADSBOT_GOOG_HTML)
        cls.ADSBOT_GOOG_MP3 = json.loads(_config.DATA_ADSBOT_GOOG_MP3)
        cls.ADSBOT_GOOG_POST = json.loads(_config.DATA_ADSBOT_GOOG_POST)
        cls.SNAPSEARCH_GET = json.loads(_config.DATA_SNAPSEARCH_GET)
        cls.GOOGBOT_IGNORED = json.loads(_config.DATA_GOOGBOT_IGNORED)
        cls.MSNBOT_MATCHED = json.loads(_config.DATA_MSNBOT_MATCHED)
        cls.ESCAPE_FRAG_NULL = json.loads(_config.DATA_ESCAPE_FRAG_NULL)
        cls.ESCAPE_FRAG_VARS = json.loads(_config.DATA_ESCAPE_FRAG_VARS)
        pass  # void return

    def test_detector_call_bad_request_no_method(self):
        from SnapSearch import Detector
        detector = Detector()
        request = {'SERVER_NAME': "localhost", 'SERVER_PORT': "80"}
        self.assertFalse(detector(request))  # should *not* be intercepted
        pass  # void return

    def test_detector_call_bad_request_non_http(self):
        from SnapSearch import Detector
        detector = Detector()
        request = {'SERVER_NAME': "localhost", 'SERVER_PORT': "80",
                   'wsgi.url_scheme': "non-http", }
        self.assertFalse(detector(request))  # should *not* be intercepted
        pass  # void return

    def test_detector_call_normal_browser_firefox(self):
        from SnapSearch import Detector
        detector = Detector()
        request = self.FIREFOX_REQUEST
        self.assertFalse(detector(request))  # should *not* be intercepted
        pass  # void return

    def test_detector_call_normal_browser_safari(self):
        from SnapSearch import Detector
        detector = Detector()
        request = self.SAFARI_REQUEST
        self.assertFalse(detector(request))  # should *not* be intercepted
        pass  # void return

    def test_detector_call_search_engine_bot(self):
        from SnapSearch import Detector
        detector = Detector()
        request = self.ADSBOT_GOOG_GET
        self.assertTrue(detector(request))  # should be intercepted
        pass  # void return

    def test_detector_call_search_engine_bot_ignored_route(self):
        from SnapSearch import Detector
        detector = Detector(ignored_routes=["^\/other", "^\/ignored", ])
        request = self.GOOGBOT_IGNORED
        self.assertFalse(detector(request))  # should *not* be intercepted
        pass  # void return

    def test_detector_call_search_engine_bot_matched_route(self):
        from SnapSearch import Detector
        detector = Detector(matched_routes=["^\/other", "^\/matched", ])
        request = self.MSNBOT_MATCHED
        self.assertTrue(detector(request))  # should be intercepted
        pass  # void return

    def test_detector_call_search_engine_bot_non_matched_route(self):
        from SnapSearch import Detector
        detector = Detector(matched_routes=["^\/x", "^\/non_matched_route", ])
        request = self.MSNBOT_MATCHED
        self.assertFalse(detector(request))  # should *not* be intercepted
        pass  # void return

    def test_detector_call_search_engine_bot_post(self):
        from SnapSearch import Detector
        detector = Detector()
        request = self.ADSBOT_GOOG_POST
        self.assertFalse(detector(request))  # should *not* be intercepted
        pass  # void return

    def test_detector_call_snapsearch_bot(self):
        from SnapSearch import Detector
        detector = Detector()
        request = self.SNAPSEARCH_GET
        self.assertFalse(detector(request))  # should *not* be intercepted
        pass  # void return

    def test_detector_call_check_file_ext_eligible(self):
        from SnapSearch import Detector
        detector = Detector(check_file_extensions=True)
        request = self.ADSBOT_GOOG_HTML
        self.assertTrue(detector(request))  # should be intercepted
        pass  # void return

    def test_detector_call_check_file_ext_ineligible(self):
        from SnapSearch import Detector
        detector = Detector(check_file_extensions=True)
        request = self.ADSBOT_GOOG_MP3
        self.assertFalse(detector(request))  # should *not* be intercepted
        pass  # void return

    def test_detector_call_check_file_ext_non_existent(self):
        from SnapSearch import Detector
        detector = Detector(check_file_extensions=True)
        request = self.ADSBOT_GOOG_HTML
        self.assertTrue(detector(request))  # should be intercepted
        pass  # void return

    def test_detector_call_return_escape_frag_null(self):
        from SnapSearch import Detector
        detector = Detector()
        request = self.ESCAPE_FRAG_NULL
        self.assertEqual(detector(request), "http://localhost/snapsearch")
        pass  # void return

    def test_detector_call_return_escape_frag_vars(self):
        from SnapSearch import Detector
        detector = Detector()
        request = self.ESCAPE_FRAG_VARS
        self.assertEqual(detector(request), "http://localhost/snapsearch/path1"
                                            "?key1=value1#!/path2?key2=value2")
        pass  # void return


class TestDetectorProperties(unittest.TestCase):
    """
    Tests updating ``robots`` and ``extensions`` of a Detector object.
    """

    @classmethod
    def setUpClass(cls):
        cls.ADSBOT_GOOG_GET = json.loads(_config.DATA_ADSBOT_GOOG_GET)
        cls.ADSBOT_GOOG_MP3 = json.loads(_config.DATA_ADSBOT_GOOG_MP3)
        pass  # void return

    def test_detector_prop_update_robots(self):
        from SnapSearch import Detector, error
        detector = Detector()
        request = self.ADSBOT_GOOG_GET
        # append a robot to the white list
        self.assertTrue(detector(request))
        detector.robots['ignore'].append("Adsbot-Google")
        self.assertFalse(detector(request))
        # try to damange the structure of ``robots``
        detector.robots['ignore'] = None
        self.assertRaises(error.SnapSearchError, detector, request)
        pass  # void return

    def test_detector_prop_update_extension(self):
        from SnapSearch import Detector, error
        detector = Detector(check_file_extensions=True)
        request = self.ADSBOT_GOOG_MP3
        self.assertFalse(detector(request))
        detector.extensions['generic'].append("mp3")
        self.assertTrue(detector(request))
        # try to damange the structure of ``extensions``
        detector.extensions['generic'] = None
        self.assertRaises(error.SnapSearchError, detector, request)
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
