# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
"""
HTTP Client Middleware Library for SnapSearch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014 by SnapSearch.
:license: MIT, see LICENSE for more details.
"""

__all__ = ['Client', 'Detector', 'Interceptor', 'SnapSearchError', ]

# package metadata

__author__ = "LIU Yu"
__contact__ = "liuyu@opencps.net"
__copyright__ = 'Copyright (c) 2014 SnapSearch'
__license__ = "MIT"
__title__ = "SnapSearch"
__version__ = (0, 0, 3)

# import objects from sub-modules and re-export them here for easy access

from ._config import SNAPSEARCH_API_URL
from ._config import SNAPSEARCH_RES_DIR

from .client import Client
from .detector import Detector
from .interceptor import Interceptor
from .error import SnapSearchError
