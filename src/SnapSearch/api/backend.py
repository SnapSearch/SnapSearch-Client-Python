# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/06
#

__all__ = ['dispatch', ]


import os
import sys

import SnapSearch.error as error

from .._config import u, wsgi_to_bytes
from .response import Response


def _dispatch_via_requests(**kwds):

    # import locally to allow override
    from . import (SNAPSEARCH_API_FOLLOW_REDIRECT,
                   SNAPSEARCH_API_TIMEOUT, )

    import requests

    # HTTPS POST request
    payload = wsgi_to_bytes(kwds['payload'])
    headers = {"Content-Type": "application/json",
               "Content-Length": len(payload)}

    # HTTPS connection
    s = requests.Session()
    try:
        r = s.request(method="POST",
                      url=kwds['url'],
                      verify=kwds['ca_path'],
                      auth=(kwds['email'], kwds['key']),
                      data=payload,
                      headers=headers,
                      allow_redirects=SNAPSEARCH_API_FOLLOW_REDIRECT,
                      timeout=SNAPSEARCH_API_TIMEOUT)
    except Exception as e:
        raise error.SnapSearchConnectionError(e)
    else:
        return Response(status=r.status_code, headers=r.headers, text=r.text)
    finally:
        s.close()

    pass  # void return


def _dispatch_via_pycurl(**kwds):

    # import locally to allow override
    from . import (SNAPSEARCH_API_FOLLOW_REDIRECT,
                   SNAPSEARCH_API_TIMEOUT, )

    # HTTPS connection
    import pycurl
    c = pycurl.Curl()
    c.setopt(pycurl.URL, kwds['url'])

    # HTTPS POST request
    payload = wsgi_to_bytes(kwds['payload'])
    headers = ["Content-Type: application/json",
               "Content-Length: %d" % len(payload)]

    c.setopt(pycurl.POST, True)
    c.setopt(pycurl.HTTPHEADER, headers)
    c.setopt(pycurl.POSTFIELDS, payload)

    # HTTPS auth
    c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
    c.setopt(pycurl.USERPWD, "%s:%s" % (kwds['email'], kwds['key']))
    c.setopt(pycurl.CAINFO, kwds['ca_path'])
    c.setopt(pycurl.SSL_VERIFYPEER, True)
    c.setopt(pycurl.SSL_VERIFYHOST, 2)

    c.setopt(pycurl.ENCODING, "")
    c.setopt(pycurl.FOLLOWLOCATION, SNAPSEARCH_API_FOLLOW_REDIRECT)
    c.setopt(pycurl.TIMEOUT, SNAPSEARCH_API_TIMEOUT)

    buffer = bytearray()
    c.setopt(pycurl.HEADER, True)
    c.setopt(pycurl.WRITEFUNCTION, buffer.extend)

    try:
        c.perform()
        # response status
        eos = buffer.find(b"\r\n")  # end of status line
        strip = lambda b: bytes(b).strip()
        preamble = tuple(map(strip, buffer[:eos].split(b" ", 2)))
        if len(preamble) < 2:
            raise error.SnapSearchError(
                "malformed response from SnapSearch backend")
        status_code = int(preamble[1])
        # response headers
        eoh = buffer.find(b"\r\n\r\n")  # end of header lines
        strip_kv = lambda kv: (kv[0].strip().lower().decode("utf-8"),
                               kv[1].strip().decode("utf-8"))
        split_cma = lambda b: strip_kv(bytes(b).split(b":", 1))
        headers = dict(map(split_cma, buffer[eos + 2: eoh].splitlines()))
        # response content
        text = bytes(buffer[eoh + 4:]).strip().decode("utf-8")
    except pycurl.error as e:
        raise error.SnapSearchConnectionError(e)
    except:
        raise error.SnapSearchError(
            "malformed response from SnapSearch backend")
    else:
        return Response(status=status_code, headers=headers, text=text)
    finally:
        c.close()

    pass  # void return


# unified HTTP library interface
dispatch = None
httpinfo = None

# preferred HTTP library
try:
    import requests
except ImportError:
    pass  # no raise
else:
    if not dispatch:
        dispatch = _dispatch_via_requests
        httpinfo = ("requests", requests.__version__)
    pass

# fallback HTTP library
try:
    import pycurl
except ImportError:
    pass  # no raise
else:
    if not dispatch:
        dispatch = _dispatch_via_pycurl
        httpinfo = ("pycurl", pycurl.version)
    pass

# failed all options
if not dispatch:
    raise error.SnapSearchDependencyError(
        "missing HTTP library, requires ``requests`` or ``pycurl``")
