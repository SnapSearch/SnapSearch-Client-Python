# -*- coding: utf-8 -*-
"""
    SnapSearch.error
    ~~~~~~~~~~~~~~~~

    :copyright: (c) 2014 by SnapSearch.
    :license: MIT, see LICENSE for more details.
"""


class SnapSearchError(Exception):
    """
    Common base class for all SnapSearch errros.
    """

    def __init__(self, *args, **kwds):
        super(SnapSearchError, self).__init__(*args)
        self.__data = kwds
        pass  # void return

    def __getattr__(self, name):
        if name in self.__data:
            return self.__data[name]
        return getattr(super(SnapSearchError, self), name)

    pass


class SnapSearchConnectionError(SnapSearchError):
    """
    Cannot communicate with SnapSearch backend service.
    """
    pass


class SnapSearchDependencyError(SnapSearchError):
    """
    Cannot import package(s) required by SnapSearch.
    """
    pass
