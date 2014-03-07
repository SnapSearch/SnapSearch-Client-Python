#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/06
#

__all__ = ['TestInterceptorMethods', ]


import os
import sys

try:
    from . import _config
    from ._config import unittest
except (ValueError, ImportError):
    import _config
    from _config import unittest


class TestInterceptorMethods(unittest.TestCase):

    def setUp(self):
        pass  # void return

    def test_interceptor_init(self):
        pass  # void return

    def test_interceptor_intercept(self):
        pass  # void return

    def test_interceptor_callback(self):
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
