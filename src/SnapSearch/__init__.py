# -*- coding: utf-8 -*-
"""
    SnapSearch
    ~~~~~~~~~~

    Pythonic HTTP Client and Middleware Library for `SnapSearch`_.

    .. _`SnapSearch`: https://snapsearch.io/

    :copyright: 2014 by `SnapSearch`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['Client',
           'Detector',
           'Interceptor', ]


# package metadata

__author__ = "LIU Yu"
__contact__ = "liuyu@opencps.net"
__copyright__ = 'Copyright (c) 2014 SnapSearch'
__license__ = "MIT"
__title__ = "SnapSearch"
__version__ = (0, 0, 8)

# import objects from sub-modules and re-export them as top-level objects

from .client import Client
from .detector import Detector
from .interceptor import Interceptor
