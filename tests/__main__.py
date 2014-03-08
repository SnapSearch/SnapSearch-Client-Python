# -*- coding: utf-8 -*-
"""
    SnapSearch.tests.__main__
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = []


from . import test_suite
from ._config import unittest

if __name__ == '__main__':
    import os.path
    import sys
    # local SnapSearch package takes precedence
    sys.path.insert(0, os.path.join(os.path.curdir, "src"))
    sys.path.insert(0, os.path.join(os.path.curdir))
    unittest.main(defaultTest='test_suite')
