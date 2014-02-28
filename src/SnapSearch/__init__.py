# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
"""
HTTP Client Middleware Library for SnapSearch
"""

__all__ = ['Client', 'Detector', 'Interceptor', ]

__author__ = "LIU Yu"
__contact__ = "pineapple.liu@gmail.com"
__license__ = "MIT"
__version__ = (0, 0, 1)

from .client import Client
from .detector import Detector
from .interceptor import Interceptor
