# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/05
#

__all__ = []

import atexit
import os
import os.path
import shutil
import sys
import tempfile

# package names unification

try:
    # python 2.6+
    import json
except ImportError:
    # python 2.5
    import simplejson as json

try:
    # python 2.6
    import unittest2 as unittest
except ImportError:
    # python 2.7+
    import unittest

# utilities for managing package data

DATA_DIR = os.path.dirname(__file__)


def load_data(name):
    """
    Load text resource from package data.
    """
    return open(os.path.join(DATA_DIR, name), 'rb').read()


# utilities for managing temporary files

TEMP_DIR = tempfile.mkdtemp()


def save_temp(name, data=b"", mode=0o666):
    """
    Writes data to a temporary file in the file system. Returns the full path
    to the temporary file on success, and None otherwise.
    """
    path = os.path.join(TEMP_DIR, name)
    try:
        with open(path, 'wb') as f:
            f.write(data)
            f.close()
        os.chmod(path, mode)
        if not os.access(path, os.F_OK | os.R_OK | os.W_OK):
            return None
        return path
    except:
        pass
    return None


def cleanup():
    """
    Erases temporary files and directories created during the test.
    """
    shutil.rmtree(TEMP_DIR)
    pass


atexit.register(cleanup)


# pre-fetched data

DATA_CACERT_PEM = load_data("cacert.pem").decode("utf-8")
DATA_EXTENSIONS_JSON = load_data("extensions.json").decode("utf-8")
DATA_ROBOTS_JSON = load_data("robots.json").decode("utf-8")

DATA_FIREFOX_REQUEST = load_data("req_firefox.json").decode("utf-8")
DATA_SAFARI_REQUEST = load_data("req_safari.json").decode("utf-8")
DATA_ESCAPE_FRAG_NULL = load_data("req_escape_frag_null.json").decode("utf-8")
DATA_ESCAPE_FRAG_VARS = load_data("req_escape_frag_vars.json").decode("utf-8")
DATA_MSNBOT_MATCHED = load_data("req_msnbot_matched.json").decode("utf-8")

DATA_SNAPSEARCH_GET = load_data("req_snapsearch_get.json").decode("utf-8")

DATA_ADSBOT_GOOG_GET = load_data("req_adsbot_goog_get.json").decode("utf-8")
DATA_ADSBOT_GOOG_HTML = load_data("req_adsbot_goog_html.json").decode("utf-8")
DATA_ADSBOT_GOOG_MP3 = load_data("req_adsbot_goog_mp3.json").decode("utf-8")
DATA_ADSBOT_GOOG_POST = load_data("req_adsbot_goog_post.json").decode("utf-8")

DATA_GOOGBOT_IGNORED = load_data("req_googbot_ignored.json").decode("utf-8")
DATA_MSNBOT_MATCHED = load_data("req_msnbot_matched.json").decode("utf-8")


# preliminary tests
class TestPackageIntegrity(unittest.TestCase):
    """
    Tests package availability and components.
    """

    def test_environ(self):
        self.assertTrue(os.path.isdir(DATA_DIR))
        self.assertTrue(os.path.isdir(TEMP_DIR))
        pass

    def test_package(self):
        import SnapSearch
        self.assertTrue(SnapSearch.__version__ >= (0, 0, 4))
        self.assertTrue(isinstance(SnapSearch.Client, object))
        self.assertTrue(isinstance(SnapSearch.Detector, object))
        self.assertTrue(isinstance(SnapSearch.Interceptor, object))
        self.assertTrue(isinstance(SnapSearch.SnapSearchError, object))
        pass

    def test_types_error_base(self):
        from SnapSearch import SnapSearchError
        e = SnapSearchError("base error", code=100)
        self.assertEqual(e.code, 100)
        self.assertRaises(AttributeError, lambda: e.no_such_attr)
        pass  # void return

    def test_types_error_connection(self):
        from SnapSearch import SnapSearchConnectionError
        ce = SnapSearchConnectionError("connection error", status=404)
        self.assertEqual(ce.status, 404)
        pass  # void return

    def test_types_error_dependency(self):
        from SnapSearch import SnapSearchDependencyError
        de = SnapSearchDependencyError("import error", requires=["pycurl", ])
        self.assertEqual(de.requires[0], "pycurl")
        pass  # void return

    pass
