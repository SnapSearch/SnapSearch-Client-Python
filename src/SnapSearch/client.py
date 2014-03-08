# -*- coding: utf-8 -*-
"""
    SnapSearch.client
    ~~~~~~~~~~~~~~~~~

    :copyright: 2014 by `SnapSearch <https://snapsearch.io/>`_
    :license: MIT, see LICENSE for more details.

    :author: `LIU Yu <liuyu@opencps.net>`_
    :date: 2014/03/08
"""

__all__ = ['Client', ]


import json
import os
import sys

import SnapSearch.api as api
import SnapSearch.error as error


class Client(object):
    """
    Dispatches a URL to SnapSearch backend service, and receives a response
    containing search engine optimized representation of the URL's target.
    """

    # private properties
    __slots__ = ['__api_email', '__api_key', '__request_parameters',
                 '__api_url', '__ca_path', ]

    def __init__(self, api_email, api_key, request_parameters={},
                 api_url=None, ca_path=None):
        """
        :param api_email: registered email as username for authentication
            against the SnapSearch backend service.
        :param api_key: api key as password for authentication against the
            SnapSearch backend service.

        Optional arguments:

        :param request_parameters: ``dict`` of parameters to be json-serialized
            and sent to SnapSearch backend service.
        :param api_url: URL to SnapSearch backend service.
        :param ca_path: absolute path to an external CA bundle file.

        :raises error.SnapSearchError: if ``api_url`` uses a non-https scheme
            (i.e. not starting with ``"https://"``).
        :raises error.SnapSearchError: if ``ca_path`` is either invalid or
            inaccessible.
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
        :param current_url: URL that the search engine robot is currently
            trying to access.

        :returns: the response from SnapSearch backend service, or ``None``
            if the ``code`` field of the response ``body`` is neither
            ``"success"`` nor ``"validation_error"``.

        :raises error.SnapSearchError: if either the ``status`` or ``headers``
            property of the response is empty.
        :raises error.SnapSearchError: if the response ``body`` is malformed
            (i.e. not containing fields ``"code"`` and ``"content"``).
        :raises error.SnapSearchError: if the ``code`` field of the response
            ``body`` equals ``"validation_error"``.
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
