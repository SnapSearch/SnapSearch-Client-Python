# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/03
#
"""
Test Suite for SnapSearch-Client-Python
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
