# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
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

    # private properties
    __slots__ = ['__detector', '__client', '__before', '__after', ]

    def __init__(self, client, detector):
        """
        Keyword arguments:

        :param client: Client object
        :param detector: Detector object
        """
        assert(isinstance(client, Client) and isinstance(detector, Detector))
        self.__client = client
        self.__detector = detector
        pass  # void return

    def intercept(self):
        """
        """
        return None

    pass
