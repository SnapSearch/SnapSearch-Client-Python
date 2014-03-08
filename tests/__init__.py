# -*- coding: utf-8 -*-
"""
    SnapSearch.tests
    ~~~~~~~~~~~~~~~~

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['test_suite', ]


from . import (test_client,
               test_detector,
               test_interceptor,
               test_wsgi,
               test_cgi)

from ._config import unittest, TestPackageIntegrity


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().
                  loadTestsFromTestCase(TestPackageIntegrity))
    for pkg in (test_client,
                test_detector,
                test_interceptor,
                test_wsgi,
                test_cgi):
        suite.addTest(pkg.test_suite())
    return suite
