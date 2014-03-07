# -*- coding: utf-8 -*-
"""
    SnapSearch-Client-Python
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Pythonic HTTP Client and Middleware for `SnapSearch`_.

    .. _`SnapSearch`: https://snapsearch.io/

    :copyright: (c) 2014 by SnapSearch.
    :license: MIT, see LICENSE for more details.
"""

__all__ = ['Client',
           'Detector',
           'Interceptor',
           'SnapSearchError',
           'SnapSearchConnectionError',
           'SnapSearchDependencyError', ]


# package metadata

__author__ = "LIU Yu"
__contact__ = "liuyu@opencps.net"
__copyright__ = 'Copyright (c) 2014 SnapSearch'
__license__ = "MIT"
__title__ = "SnapSearch"
__version__ = (0, 0, 6)

# import objects from sub-modules and re-export them as top-level objects

from .client import Client
from .detector import Detector
from .interceptor import Interceptor
from .error import *
