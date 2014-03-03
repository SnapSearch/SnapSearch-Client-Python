# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
"""
HTTP Client Middleware Library for SnapSearch
"""

__all__ = ['Client', 'Detector', 'Interceptor', 'SnapSearchError', ]

# package metadata

__author__ = "LIU Yu"
__contact__ = "liuyu@opencps.net"
__license__ = "MIT"
__version__ = (0, 0, 2)

# import essential objects and re-export them here for easy access

from .client import Client
from .detector import Detector
from .interceptor import Interceptor
from .error import SnapSearchError
