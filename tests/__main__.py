# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

__all__ = []

from . import test_suite
from ._config import unittest

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
