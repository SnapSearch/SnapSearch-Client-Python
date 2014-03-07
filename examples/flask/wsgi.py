__all__ = ['Middleware', ]


import json
import os
import sys

from werkzeug.wsgi import ClosingIterator


class Middleware(object):

    def __init__(self, application, interceptor):
        #
        self.application = application
        self.interceptor = interceptor
        pass

    def __call__(self, environ, start_response):

        def start_interception(status, response_headers, exc_info=None):

            print("middleware:", "start interception")
            response = self.interceptor(environ)

            # <TODO>
            if not response:
                print("middleware:", "no need to intercept")
            else:
                print("middleware:", "intercepted")
                print(response)
            # </TODO>

            return start_response(status, response_headers, exc_info)

        return ClosingIterator(self.application(environ, start_interception))

    pass
