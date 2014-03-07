# -*- coding: utf-8 -*-
"""
    SnapSearch.api.response
    ~~~~~~~~~~~~~~~~~~~~~~~

    wrapper for response from SnapSearch backend service

    :copyright: (c) 2014 by SnapSearch.
    :license: MIT, see LICENSE for more details.
"""


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
            self.__headers = self.__raw_response.get('headers', None)
        return self.__headers

    @property
    def body(self):
        """
        response body (``dict``)
        """
        if not self.__body:
            self.__body = self.__raw_response.get('body', "")
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
