# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.

# This has to be the first statement.
from __future__ import with_statement

import os
import sys

# Use unittest2 on versions older than Python 2.7.
if sys.version_info[0] < 3 and sys.version_info[1] < 7:
    from unittest2 import TestCase, main
else:
    from unittest import TestCase, main
