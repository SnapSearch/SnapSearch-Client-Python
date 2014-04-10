# -*- coding: utf-8 -*-
"""
    SnapSearch.api.response
    ~~~~~~~~~~~~~~~~~~~~~~~

    wrapper for response from SnapSearch backend service

    :copyright: 2014 by `SnapSearch <https://snapsearch.io/>`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['Response', 'message_extractor', ]


import functools

from .._compat import u, HTTP_STATUS_CODES


def _extract_message(response_body):

    # http status code
    code = response_body.get('status', 200)
    status = ("%d %s" % (code, HTTP_STATUS_CODES[code])).encode("utf-8")

    # response body
    payload = response_body.get('html', u("")).encode("utf-8")

    # response headers
    headers = []
    for item in response_body.get('headers', []):

        # bad entries
        if not isinstance(item, dict):
            continue
        if "name" not in item:
            continue
        if "value" not in item:
            continue

        # candidate entry
        tup = (str(item['name']).lower().encode("utf-8"),
               str(item['value']).encode("utf-8"))

        # selected entry
        headers.append(tup)

    return {'status': status, 'headers': headers, 'html': payload}


def message_extractor(func):
    """
    Decorator for data extracting functions requiring the HTTP message fields
    from a raw response body. This is an input preprocessing decorator for the
    implementation of ``response_callback`` used in application bindings.
    """
    def wrapper(response_body):
        return func(_extract_message(response_body))
    return functools.update_wrapper(wrapper, func)


class Response(object):
    """
    Wraps an HTTP response from SnapSearch's backend service.
    """

    @property
    def status(self):
        """
        HTTP status code (``int``)
        """
        if not self.__status:
            self.__status = int(self.__raw_response.get('status', 0))
        return self.__status

    @property
    def headers(self):
        """
        HTTP headers (``dict``)
        """
        if not self.__headers:
            self.__headers = self.__raw_response.get('headers', {})
        return self.__headers

    @property
    def body(self):
        """
        response body (``dict``)
        """
        if not self.__body:
            self.__body = self.__raw_response.get('body', {})
        return self.__body

    # private properties
    __slots__ = ['__raw_response', '__status', '__headers', '__body', ]

    def __init__(self, **kwds):
        super(Response, self).__init__()
        self.__status = None
        self.__headers = None
        self.__body = None
        self.__raw_response = kwds
        pass  # void return

    pass
