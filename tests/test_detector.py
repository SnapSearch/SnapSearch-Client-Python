#!/usr/bin/env python
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

# future import should be the beginning line
from __future__ import with_statement

__all__ = ['TestDetectorConstruction', ]

import os
import sys

from os.path import abspath, join

try:
    from . import _config
    from ._config import unittest
except (ValueError, ImportError):
    import _config
    from _config import unittest


class TestDetectorConstruction(unittest.TestCase):
    """
    Tests different ways to construct a Detector object.
    """
    def setUp(self):
        self.FN_ROBOTS_JSON = _config.save_temp(
            "robots.json", _config.DATA_ROBOTS_JSON)
        self.FN_EXTENSIONS_JSON = _config.save_temp(
            "extensions.json", _config.DATA_EXTENSIONS_JSON)
        pass

    def test_default_construction(self):
        from SnapSearch import Detector
        d = Detector()
        # make sure the default robots.json is loaded
        self.assertTrue(hasattr(d, 'robots'))
        self.assertTrue(d.robots)
        self.assertTrue('Bingbot' in d.robots['match'])
        # make sure the default extensions.json is loaded
        self.assertTrue(hasattr(d, 'extensions'))
        self.assertTrue(d.extensions)
        self.assertTrue('html' in d.extensions['generic'])
        pass

    def test_custom_robots_json(self):
        from SnapSearch import Detector
        # correct construction with custom robots.json
        d = Detector(robots_json=self.FN_ROBOTS_JSON)
        self.assertTrue(d.robots)
        self.assertTrue('Testbot' in d.robots['match'])
        pass

    def test_custom_extensions_json(self):
        from SnapSearch import Detector
        # specified extensions.json but check_file_extensions is false
        self.assertRaises(AssertionError, Detector,
                          check_file_extensions=False,
                          extensions_json=self.FN_EXTENSIONS_JSON)
        # correct construction with custom extensions.json
        d = Detector(check_file_extensions=True,
                     extensions_json=self.FN_EXTENSIONS_JSON)
        self.assertTrue(d.extensions)
        self.assertTrue('test' in d.extensions['generic'])
        pass

    pass


def test_suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(eval(c)) for c in __all__])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
