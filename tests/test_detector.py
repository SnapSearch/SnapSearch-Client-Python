#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/03
#

# future import should be the beginning line
from __future__ import with_statement

__all__ = ['TestDetectorInit', 'TestDetectorMethod', 'TestDetectorProperty', ]

try:
    from . import _config
    from ._config import json, unittest
except (ValueError, ImportError):
    import _config
    from _config import json, unittest


class TestDetectorInit(unittest.TestCase):
    """
    Tests different ways to initialize a Detector object.
    """
    def setUp(self):
        # save local data to temporary files
        self.EXTERNAL_ROBOTS_JSON = _config.save_temp(
            "robots.json", _config.DATA_ROBOTS_JSON.encode("utf-8"))
        self.EXTERNAL_EXTENSIONS_JSON = _config.save_temp(
            "extensions.json", _config.DATA_EXTENSIONS_JSON.encode("utf-8"))
        pass  # void return

    def test_detector_init(self):
        # initialize with default arguments
        from SnapSearch import Detector
        d = Detector()
        # make sure the default `robots.json` is loaded
        self.assertTrue(hasattr(d, 'robots'))
        self.assertTrue(d.robots)
        self.assertTrue("Bingbot" in d.robots['match'])
        # make sure the default `extensions.json` is loaded
        self.assertTrue(hasattr(d, 'extensions'))
        self.assertTrue(d.extensions)
        self.assertTrue("html" in d.extensions['generic'])
        pass  # void return

    def test_detector_init_external_robots_json(self):
        # initialize with external `robots.json`
        from SnapSearch import Detector
        d = Detector(robots_json=self.EXTERNAL_ROBOTS_JSON)
        self.assertTrue(d.robots)
        self.assertTrue("Testbot" in d.robots['match'])
        pass  # void return

    def test_detector_init_external_extensions_json(self):
        # initialize with external `extensions.json`
        from SnapSearch import Detector
        d = Detector(check_file_extensions=True,
                     extensions_json=self.EXTERNAL_EXTENSIONS_JSON)
        self.assertTrue(d.extensions)
        self.assertTrue("test" in d.extensions['generic'])
        # specified `extensions.json` but `check_file_extensions` is False
        self.assertRaises(AssertionError, Detector,
                          check_file_extensions=False,
                          extensions_json=self.EXTERNAL_EXTENSIONS_JSON)
        pass  # void return

    pass


class TestDetectorMethod(unittest.TestCase):
    """
    Test ``detect()`` and ``get_encoded_url()`` with different requests.
    """
    def setUp(self):
        self.FIREFOX_REQUEST = json.loads(_config.DATA_FIREFOX_REQUEST)
        self.SAFARI_REQUEST = json.loads(_config.DATA_SAFARI_REQUEST)
        self.ADSBOT_GOOG_GET = json.loads(_config.DATA_ADSBOT_GOOG_GET)
        self.ADSBOT_GOOG_HTML = json.loads(_config.DATA_ADSBOT_GOOG_HTML)
        self.ADSBOT_GOOG_MP3 = json.loads(_config.DATA_ADSBOT_GOOG_MP3)
        self.ADSBOT_GOOG_POST = json.loads(_config.DATA_ADSBOT_GOOG_POST)
        self.SNAPSEARCH_GET = json.loads(_config.DATA_SNAPSEARCH_GET)
        self.GOOGBOT_IGNORED = json.loads(_config.DATA_GOOGBOT_IGNORED)
        self.MSNBOT_MATCHED = json.loads(_config.DATA_MSNBOT_MATCHED)
        self.ESCAPE_FRAG_NULL = json.loads(_config.DATA_ESCAPE_FRAG_NULL)
        self.ESCAPE_FRAG_VARS = json.loads(_config.DATA_ESCAPE_FRAG_VARS)
        pass  # void return

    def test_detector_detect_bad_request_no_method(self):
        from SnapSearch import Detector
        d = Detector(request={'SERVER_NAME': "localhost", 'SERVER_PORT': "80"})
        self.assertFalse(d.detect())  # should *not* be intercepted
        pass  # void return

    def test_detector_detect_bad_request_non_http(self):
        from SnapSearch import Detector
        d = Detector(request={'SERVER_NAME': "localhost", 'SERVER_PORT': "80",
                              'wsgi.url_scheme': "non-http", })
        self.assertFalse(d.detect())  # should *not* be intercepted
        pass  # void return

    def test_detector_detect_normal_browser_firefox(self):
        from SnapSearch import Detector
        d = Detector(request=self.FIREFOX_REQUEST)
        self.assertFalse(d.detect())  # should *not* be intercepted
        pass  # void return

    def test_detector_detect_normal_browser_safari(self):
        from SnapSearch import Detector
        d = Detector(request=self.SAFARI_REQUEST)
        self.assertFalse(d.detect())  # should *not* be intercepted
        pass  # void return

    def test_detector_detect_search_engine_bot(self):
        from SnapSearch import Detector
        d = Detector(request=self.ADSBOT_GOOG_GET)
        self.assertTrue(d.detect())  # should be intercepted
        pass  # void return

    def test_detector_detect_search_engine_bot_ignored_route(self):
        from SnapSearch import Detector
        d = Detector(ignored_routes=['^\/other', '^\/ignored', ],
                     request=self.GOOGBOT_IGNORED)
        self.assertFalse(d.detect())  # should *not* be intercepted
        pass  # void return

    def test_detector_detect_search_engine_bot_matched_route(self):
        from SnapSearch import Detector
        d = Detector(matched_routes=['^\/other', '^\/matched', ],
                     request=self.MSNBOT_MATCHED)
        self.assertTrue(d.detect())  # should be intercepted
        pass  # void return

    def test_detector_detect_search_engine_bot_non_matched_route(self):
        from SnapSearch import Detector
        d = Detector(matched_routes=['^\/other', '^\/non_matched_route', ],
                     request=self.MSNBOT_MATCHED)
        self.assertFalse(d.detect())  # should *not* be intercepted
        pass  # void return

    def test_detector_detect_search_engine_bot_post(self):
        from SnapSearch import Detector
        d = Detector(request=self.ADSBOT_GOOG_POST)
        self.assertEqual(d.detect(), False)  # should *not* be intercepted
        pass  # void return

    def test_detector_detect_snapsearch_bot(self):
        from SnapSearch import Detector
        d = Detector(request=self.SNAPSEARCH_GET)
        self.assertFalse(d.detect())  # should *not* be intercepted
        pass  # void return

    def test_detector_detect_check_file_ext_eligible(self):
        from SnapSearch import Detector
        d = Detector(check_file_extensions=True,
                     request=self.ADSBOT_GOOG_HTML)
        self.assertTrue(d.detect())  # should be intercepted
        pass  # void return

    def test_detector_detect_check_file_ext_ineligible(self):
        from SnapSearch import Detector
        d = Detector(check_file_extensions=True,
                     request=self.ADSBOT_GOOG_MP3)
        self.assertFalse(d.detect())  # should *not* be intercepted
        pass  # void return

    def test_detector_detect_check_file_ext_non_existent(self):
        from SnapSearch import Detector
        d = Detector(check_file_extensions=True,
                     request=self.ADSBOT_GOOG_HTML)
        self.assertTrue(d.detect())  # should be intercepted
        pass  # void return

    def test_detector_get_encoded_url_escape_frag_null(self):
        from SnapSearch import Detector
        d = Detector(request=self.ESCAPE_FRAG_NULL)
        self.assertTrue(d.detect())  # should be intercepted
        self.assertEqual(d.get_encoded_url(), "http://localhost/snapsearch")
        pass  # void return

    def test_detector_get_encoded_url_escape_frag_vars(self):
        from SnapSearch import Detector
        d = Detector(request=self.ESCAPE_FRAG_VARS)
        self.assertTrue(d.detect())  # should be intercepted
        self.assertEqual(d.get_encoded_url(), "http://localhost/snapsearch"
                         "/path1?key1=value1#!/path2?key2=value2")
        pass  # void return


class TestDetectorProperty(unittest.TestCase):
    """
    Tests updating ``robots`` and ``extensions`` of a Detector object.
    """
    def setUp(self):
        self.ADSBOT_GOOG_GET = json.loads(_config.DATA_ADSBOT_GOOG_GET)
        self.ADSBOT_GOOG_MP3 = json.loads(_config.DATA_ADSBOT_GOOG_MP3)
        pass  # void return

    def test_detector_prop_update_robots(self):
        from SnapSearch import Detector
        d = Detector(request=self.ADSBOT_GOOG_GET)
        # append a robot to the white list
        self.assertTrue(d.detect())
        d.robots['ignore'].append("Adsbot-Google")
        self.assertFalse(d.detect())
        # try to damange the structure of ``robots``
        d.robots['ignore'] = None
        self.assertRaises(TypeError, d.detect)
        pass  # void return

    def test_detector_prop_update_extension(self):
        from SnapSearch import Detector
        d = Detector(check_file_extensions=True,
                     request=self.ADSBOT_GOOG_MP3)
        self.assertFalse(d.detect())
        d.extensions['generic'].append("mp3")
        self.assertTrue(d.detect())
        # try to damange the structure of ``extensions``
        d.extensions['generic'] = None
        self.assertRaises(TypeError, d.detect)
        pass  # void return

    pass


def test_suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(eval(c)) for c in __all__])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
