# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/06
#


class Response(object):
    """
    Wraps an HTTP response from SnapSearch's backend service.
    """

    @property
    def status(self):
        """
        HTTP status code
        """
        if not self.__status:
            self.__status = int(self.__raw_response.get('status', 0))
        return self.__status

    @property
    def headers(self):
        """
        HTTP headers as ``dict``
        """
        if not self.__headers:
            self.__headers = self.__raw_response.get('headers', None)
        return self.__headers

    @property
    def text(self):
        """
        Content of response
        """
        if not self.__text:
            self.__text = self.__raw_response.get('text', "")
        return self.__text

    # private properties
    __slots__ = ['__raw_response', '__status', '__headers', '__text', ]

    def __init__(self, **kwds):
        super(Response, self).__init__()
        self.__status = None
        self.__headers = None
        self.__text = None
        self.__raw_response = kwds
        pass  # void return

    pass
