# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 SnapSearch
# Licensed under the MIT license.
#
# :author: LIU Yu <liuyu@opencps.net>
# :date: 2014/03/06
#

__all__ = ['Client', ]

import json
import os
import sys

import SnapSearch.api as api
import SnapSearch.error as error


class Client(object):
    """
    ``Client`` dispatches the SnapSearch backend service and retrieves a
    snapshot of the URL being accessed by the incoming HTTP request.
    """

    # private properties
    __slots__ = ['__api_email', '__api_key', '__request_parameters',
                 '__api_url', '__ca_path', ]

    def __init__(self, api_email, api_key, request_parameters={},
                 api_url=None, ca_path=None):
        """
        Required arguments:

        :param api_email: registered email as username for authentication
        against the SnapSearch backend service.
        :param api_key: api key as password for authentication against the
        SnapSearch backend service.

        Optional arguments:

        :param request_parameters: ``dict`` of parameters to be json-serialized
            and sent to SnapSearch backend service.
        :param api_url: URL to SnapSearch backend service.
        :param ca_path: absolute path to an external CA bundle file.
        """

        self.__api_email = api_email
        self.__api_key = api_key
        self.__request_parameters = request_parameters or {}

        self.__api_url = api_url or api.SNAPSEARCH_API_URL
        if not self.__api_url.startswith("https://"):
            raise error.SnapSearchError("``api_url`` uses non-https scheme")

        self.__ca_path = ca_path or api.DEFAULT_CA_BUNDLE_PEM
        if not os.access(self.__ca_path, os.F_OK | os.R_OK):
            raise error.SnapSearchError("``ca_path`` invalid or inaccessable")

        pass  # void return

    def __call__(self, current_url):
        """
        Required argument(s):

        :param current_url: current URL that the search engine robot is
            attempting to access.

        Returns the response from SnapSearch backend service. Raises
        ``SnapSearchError`` on failure.
        """
        self.__request_parameters['url'] = current_url
        payload = json.dumps(self.__request_parameters)

        # dispatch the request to SnapSearch backend
        r = api.dispatch(email=self.__api_email,
                         key=self.__api_key,
                         payload=payload,
                         url=self.__api_url,
                         ca_path=self.__ca_path)

        # parse response body as json data
        try:
            # HTTP status code and headers should exist
            assert(r.status and r.headers)
            # body data
            code = r.body["code"]
            content = r.body["content"]
        except Exception as e:
            raise error.SnapSearchError(
                "malformed response from SnapSearch backend")
        else:
            if code == "success":
                return content
            # something wrong with the ``request_parameters``
            if code == "validation_error":
                raise error.SnapSearchError(
                    "validation error from SnapSearch backend, check "
                    "``request_parameters`` ", code=code, message=r.body)
            # unknown error in SnapSearch backend service
            pass

        # nothing we can do
        return None

    pass
