# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/06
#

__all__ = ['Interceptor', ]


from . import Client, Detector


class Interceptor(object):
    """
    Interceptor intercepts the request and checks with the Detector if the
    request is valid for interception and then calls the Client for scraping
    and finally returns the content of the snapshot.
    """

    @property
    def client(self):
        """
        Client object
        """
        return self.__client

    @property
    def detector(self):
        """
        Detector object
        """
        return self.__detector

    @property
    def before_intercept(self):
        """
        Before interception callback
        """
        return self.__start

    @property
    def after_intercept(self):
        """
        After interception callback
        """
        return self.__end

    # private properties
    __slots__ = ['__detector', '__client', '__start', '__end', ]

    def __init__(self, client, detector, before_intercept=None,
                 after_intercept=None):
        """
        Keyword arguments:

        :param client: Client object
        :param detector: Detector object
        """

        assert(isinstance(client, Client))
        assert(isinstance(detector, Detector))
        self.__client = client
        self.__detector = detector
        self.__start = before_intercept if callable(before_intercept) else None
        self.__end = after_intercept if callable(after_intercept) else None

        pass  # void return

    def intercept(self, environ):
        """
        Keyword argument(s):

        :param environ: ``dict`` of HTTP request variables.

        Returns the snapshot if the request was scraped
        """

        raw_current_url = self.detector.detect(environ)
        if not raw_current_url:
            # request not eligible for interception
            return None

        # pre-interception callback
        if callable(self.before_intercept):
            result = self.before_intercept(raw_current_url)
            if result != raw_current_url:
                return result

        response = self.client.request(raw_current_url)

        # post-interception callback
        if callable(self.after_intercept):
            self.after_intercept(raw_current_url, response)

        return response

    pass
