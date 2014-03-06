# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

__all__ = ['Response', ]

from .._config import u


class Response(object):
    """
    Response wraps an HTTP response from SnapSearch's backend service.
    """

    @property
    def status(self):
        if not self.__status:
            self.__status = self.__raw_response.get('status', None)
        return self.__status

    @property
    def headers(self):
        if not self.__headers:
            self.__headers = self.__raw_response.get('headers', None)
        return self.__headers

    @property
    def body(self):
        if not self.__body:
            self.__body = self.__raw_response.get('body', "")
        return self.__body

    # private properties
    __slots__ = ['__raw_response', '__body', '__headers', '__status', ]

    def __init__(self, **message):
        super(Response, self).__init__()
        self.__status = None
        self.__headers = None
        self.__body = None
        self.__raw_response = message
        pass  # void return

    pass
