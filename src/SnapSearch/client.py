# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#

__all__ = ['Client', ]

import os
import sys

from ._config import SNAPSEARCH_API_URL, DEFAULT_CACERT_PEM
from ._config import json, wsgi_to_bytes, BytesIO

from .error import SnapSearchError


class Response(BytesIO):

    def get_parsed_response(self):
        return self.getvalue()

    pass


class Client(object):
    """
    Client contacts SnapSearch service and retrieves the snapshot.
    """

    # private properties
    __slots__ = ['__api_email', '__api_key', '__request_parameters',
                 '__api_url', '__ca_path', ]

    def __init__(self, api_email, api_key, request_parameters={},
                 api_url=None, ca_path=None):
        """
        Keyword arguments:

        :param api_email: email as user name for HTTP basic authentication.
        :param api_key: key as password for HTTP basic authentication.
        :param request_parameters: ``dict`` of parameters to be json-encoded
            and sent to SnapSearch service.
        :param api_url: SnapSearch API url.
        :param ca_path: absolute path to CA certificate.
        """

        self.__api_email = api_email
        self.__api_key = api_key
        self.__request_parameters = request_parameters or {}

        self.__api_url = api_url or SNAPSEARCH_API_URL
        if not self.__api_url.startswith("https://"):
            raise SnapSearchError("``api_url`` uses non-https scheme")

        self.__ca_path = ca_path or DEFAULT_CACERT_PEM
        if not os.access(self.__ca_path, os.F_OK | os.R_OK):
            raise SnapSearchError("``ca_path`` invalid or inaccessable")

        pass  # void return

    def request(self, current_url):
        """
        Keyword arguments:

        :param current_url: current URL that the robot is going to accessing.

        Returns response ``dict`` from SnapSearch

        Raises ``SnapSearchError``
        """

        # HTTP(S) request payload
        self.__request_parameters['url'] = current_url
        payload = wsgi_to_bytes(json.dumps(self.__request_parameters))
        payload_length = len(payload)

        # HTTP(S) request headers
        headers = ["Content-Type: application/json",
                   "Content-Length: %d" % payload_length]

        # HTTP(S) connection
        import pycurl
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.__api_url)

        c.setopt(pycurl.CAINFO, self.__ca_path)
        c.setopt(pycurl.SSL_VERIFYPEER, True)
        c.setopt(pycurl.SSL_VERIFYHOST, 2)

        c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
        c.setopt(pycurl.USERPWD, "%s:%s" % (self.__api_email, self.__api_key))
        c.setopt(pycurl.POST, True)
        c.setopt(pycurl.HTTPHEADER, headers)
        c.setopt(pycurl.POSTFIELDS, payload)

        c.setopt(pycurl.HEADER, True)
        c.setopt(pycurl.ENCODING, "")
        c.setopt(pycurl.CONNECTTIMEOUT, 5)
        c.setopt(pycurl.TIMEOUT, 30)

        r = Response()
        c.setopt(pycurl.WRITEFUNCTION, r.write)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.MAXREDIRS, 5)

        try:
            c.perform()
        except pycurl.error as e:
            raise SnapSearchError(e)
        else:
            pass
        finally:
            c.close()

        return r.get_parsed_response()

    pass
