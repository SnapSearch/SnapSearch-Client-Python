#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SnapSearch Client Demo (CGI)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: 2014 by `SnapSearch <https://snapsearch.io/>`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

import cgi
import cgitb
import sys


def hello_world():
    msg = b"Hello World!"
    sys.stdout.write(b"Status: 200 OK\r\n")
    sys.stdout.write(b"Content-Type: text/html; charset=utf-8\r\n")
    sys.stdout.write(b"Content-Length: ")
    sys.stdout.write(bytes(len(msg)))
    sys.stdout.write(b"\r\n\r\n")
    sys.stdout.write(msg)
    sys.stdout.write(b"\r\n")
    return 0


if __name__ == '__main__':

    # load SnapSearch API credentials
    import os
    credentials = os.environ.get('SNAPSEARCH_API_CREDENTIALS', ":")
    api_email, sep, api_key = credentials.partition(":")

    # initialize the interceptor
    from SnapSearch import Client, Detector, Interceptor
    interceptor = Interceptor(Client(api_email, api_key), Detector())

    # deploy the interceptor
    from SnapSearch.cgi import InterceptorController
    InterceptorController(interceptor).start()

    # start servicing
    sys.exit(hello_world())
