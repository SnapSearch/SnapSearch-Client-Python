# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/06
#
"""
HTTP Client Middleware Library for SnapSearch
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
