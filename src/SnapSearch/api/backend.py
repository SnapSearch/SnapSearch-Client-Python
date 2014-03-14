# -*- coding: utf-8 -*-
"""
    SnapSearch.api.backend
    ~~~~~~~~~~~~~~~~~~~~~~

    wrapper for communication with SnapSearch backend service

    :copyright: 2014 by `SnapSearch <https://snapsearch.io/>`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['dispatch', ]


import json
import os
import sys

import SnapSearch.error as error

from .._compat import b
from .response import Response


def _build_message(content):

    # import locally to allow override
    from . import SNAPSEARCH_API_ACCEPT_ENCODING, SNAPSEARCH_API_USER_AGENT

    payload = b(content)
    headers = {
        "User-Agent": SNAPSEARCH_API_USER_AGENT,
        "Accept-Encoding": SNAPSEARCH_API_ACCEPT_ENCODING,
        "Content-Type": "application/json",
        "Content-Length": len(payload)}

    return headers, payload


def _dispatch_via_requests(**kwds):

    # import locally to allow override
    from . import SNAPSEARCH_API_FOLLOW_REDIRECT, SNAPSEARCH_API_TIMEOUT

    # HTTPS connection
    import requests
    s = requests.Session()

    # HTTPS POST request
    headers, payload = _build_message(kwds['payload'])

    try:
        r = s.request(
            method="POST",
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
        return Response(
            status=r.status_code, headers=r.headers, body=json.loads(r.text))
    finally:
        s.close()

    pass  # void return


def _dispatch_via_pycurl(**kwds):

    # import locally to allow override
    from . import (
        SNAPSEARCH_API_ACCEPT_ENCODING,
        SNAPSEARCH_API_FOLLOW_REDIRECT,
        SNAPSEARCH_API_TIMEOUT, )

    # HTTPS connection
    import pycurl
    c = pycurl.Curl()
    c.setopt(pycurl.URL, kwds['url'])

    # HTTPS POST request
    headers_dict, payload = _build_message(kwds['payload'])
    headers = ["%s: %s" % (key, val) for key, val in headers_dict.items()]
    c.setopt(pycurl.POST, True)
    c.setopt(pycurl.HTTPHEADER, headers)
    c.setopt(pycurl.POSTFIELDS, payload)

    # authentication
    c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
    c.setopt(pycurl.USERPWD, "%s:%s" % (kwds['email'], kwds['key']))

    # SSL verfification
    c.setopt(pycurl.CAINFO, kwds['ca_path'])
    c.setopt(pycurl.SSL_VERIFYPEER, True)
    c.setopt(pycurl.SSL_VERIFYHOST, 2)

    # transfer parameters
    CURLOPT_ENCODING = getattr(pycurl, 'ACCEPT_ENCODING', pycurl.ENCODING)
    c.setopt(CURLOPT_ENCODING, SNAPSEARCH_API_ACCEPT_ENCODING)
    c.setopt(pycurl.FOLLOWLOCATION, SNAPSEARCH_API_FOLLOW_REDIRECT)
    c.setopt(pycurl.TIMEOUT, SNAPSEARCH_API_TIMEOUT)

    # buffer for response
    buffer_ = bytearray()
    c.setopt(pycurl.HEADER, True)
    c.setopt(pycurl.WRITEFUNCTION, buffer_.extend)

    try:
        c.perform()

        # markup buffer sections
        CRLF = b"\r\n"
        eos = buffer_.find(CRLF)  # end of status line
        eoh = buffer_.find(CRLF + CRLF)  # end of header lines

        # response status
        normalize_status = \
            lambda tup: tup[2].partition(b" ")[::2]
        status_tuple = tuple(map(
            lambda b: bytes(b.strip()),
            normalize_status(buffer_[:eos].partition(b" "))))
        status_code = int(status_tuple[0] or "0")

        # response headers
        normalize_header = \
            lambda hdr: (bytes(hdr[0].strip().lower()),
                         bytes(hdr[2].strip()))
        headers = dict(map(
            lambda b: normalize_header(b.partition(b":")),
            buffer_[eos + len(CRLF):eoh].splitlines()))

        # response content
        text = bytes(buffer_[eoh + 2 * len(CRLF):].strip()).decode()
    except pycurl.error as e:
        raise error.SnapSearchConnectionError(e)
    except Exception as e:
        raise error.SnapSearchError(
            "malformed response from SnapSearch backend")
    else:
        return Response(
            status=status_code, headers=headers, body=json.loads(text))
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
        httpinfo = ("requests", requests.__version__,
                    ("gzip", "deflate", "identity"))
    pass

# fallback HTTP library
try:
    import pycurl
except ImportError:
    pass  # no raise
else:
    if not dispatch:
        dispatch = _dispatch_via_pycurl
        httpinfo = ("pycurl", pycurl.version,
                    ("gzip", "deflate", "identity"))
    pass

# failed all options
if not dispatch:
    raise error.SnapSearchDependencyError(
        "missing HTTP library, requires ``requests`` or ``pycurl``")
