# -*- coding: utf-8 -*-
"""
    SnapSearch.tests
    ~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by SnapSearch.
    :license: MIT, see LICENSE for more details.
"""

__all__ = ['test_suite', ]


from . import (test_client, test_detector, test_interceptor)
from ._config import unittest, TestPackageIntegrity


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().
                  loadTestsFromTestCase(TestPackageIntegrity))
    for pkg in (test_client, test_detector, test_interceptor):
        suite.addTest(pkg.test_suite())
    return suite
