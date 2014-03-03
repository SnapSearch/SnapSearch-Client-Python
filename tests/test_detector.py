#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

# future import should be the beginning line
from __future__ import with_statement

__all__ = ['TestDetectorInit', 'TestDetectorDetect', ]

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
        self.CUSTOM_ROBOTS_JSON = _config.save_temp(
            "robots.json", _config.DATA_ROBOTS_JSON.encode('utf-8'))
        self.CUSTOM_EXTENSIONS_JSON = _config.save_temp(
            "extensions.json", _config.DATA_EXTENSIONS_JSON.encode('utf-8'))
        pass  # void return

    def test_default_init(self):
        # initialize with default arguments
        from SnapSearch import Detector
        d = Detector()
        # make sure the default `robots.json` is loaded
        self.assertTrue(hasattr(d, 'robots'))
        self.assertTrue(d.robots)
        self.assertTrue("Bingbot" in d.robots["match"])
        # make sure the default `extensions.json` is loaded
        self.assertTrue(hasattr(d, 'extensions'))
        self.assertTrue(d.extensions)
        self.assertTrue("html" in d.extensions["generic"])
        pass  # void return

    def test_external_robots_json(self):
        # initialize with external `robots.json`
        from SnapSearch import Detector
        d = Detector(robots_json=self.CUSTOM_ROBOTS_JSON)
        self.assertTrue(d.robots)
        self.assertTrue("Testbot" in d.robots["match"])
        pass  # void return

    def test_external_extensions_json(self):
        # initialize with external `extensions.json`
        from SnapSearch import Detector
        d = Detector(check_file_extensions=True,
                     extensions_json=self.CUSTOM_EXTENSIONS_JSON)
        self.assertTrue(d.extensions)
        self.assertTrue("test" in d.extensions["generic"])
        # specified `extensions.json` but `check_file_extensions` is False
        self.assertRaises(AssertionError, Detector,
                          check_file_extensions=False,
                          extensions_json=self.CUSTOM_EXTENSIONS_JSON)
        pass  # void return

    pass


class TestDetectorDetect(unittest.TestCase):
    """
    Test detection with different HTTP/HTTPS requests.
    """
    def setUp(self):
        self.FIREFOX_REQUEST = json.loads(_config.DATA_FIREFOX_REQUEST)
        pass  # void return

    def test_normal_browser(self):
        from SnapSearch import Detector
        d = Detector(request=self.FIREFOX_REQUEST)
        self.assertFalse(d.detect())
        pass  # void return

    pass


def test_suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(eval(c)) for c in __all__])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
