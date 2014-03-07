# -*- coding: utf-8 -*-
"""
    SnapSearch.interceptor
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by SnapSearch.
    :license: MIT, see LICENSE for more details.
"""

__all__ = ['Interceptor', ]


from . import Client, Detector


class Interceptor(object):
    """
    ``Interceptor`` intercepts the incoming HTTP request and depends on an
    associated ``Detector`` object to detect for search engine robots. If the
    request is valid for interception, the other associated ``Client`` object
    will dispatch the request to SnapSearch backend service for scraping and
    finally returning the content of a snapshot.
    """

    @property
    def client(self):
        """
        associated ``Client`` object
        """
        return self.__client

    @property
    def detector(self):
        """
        associated ``Detector`` object
        """
        return self.__detector

    @property
    def before_intercept(self):
        """
        pre-interception callback object
        """
        return self.__start

    @property
    def after_intercept(self):
        """
        post-interception callback object
        """
        return self.__end

    # private properties
    __slots__ = ['__detector', '__client', '__start', '__end', ]

    def __init__(self, client, detector, before_intercept=None,
                 after_intercept=None):
        """
        Required arguments:

        :param client: initialized ``Client`` object to associate
        :param detector: initialized ``Detector`` object to associate

        Optional arguments:

        :param before_intercept: pre-interception callback object with
            signature ``__call__(url) -> result``
        :param after_intercept: post-interception callable object with
            signature ``__call__(url, response) -> None``
        """

        # required arguments
        assert(isinstance(client, Client) and isinstance(detector, Detector))
        self.__client = client
        self.__detector = detector

        # optional arguments
        self.__start = before_intercept if callable(before_intercept) else None
        self.__end = after_intercept if callable(after_intercept) else None

        pass  # void return

    def __call__(self, request):
        """
        Required argument(s):

        :param request: incoming HTTP request as a ``dict`` of variables.

        Returns the response from SnapSearch backend service. The response is
            a snapshot of the requested URL on success.
        """

        # check for the eligibility of interception
        raw_current_url = self.detector(request)
        if not raw_current_url:
            return None

        # invoke pre-interception callback
        if callable(self.before_intercept):
            result = self.before_intercept(raw_current_url)
            # allow pre-interception callback to shortcut the interception
            if isinstance(result, dict):
                return result

        # dispatch backend service
        response = self.client(raw_current_url)

        # invoke post-interception callback
        if callable(self.after_intercept):
            # why don't we allow post-interception callback to override the
            # response from the backend service?
            self.after_intercept(raw_current_url, response)

        return response

    pass
