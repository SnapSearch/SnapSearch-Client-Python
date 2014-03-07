__all__ = ['Middleware', ]


import json
import os
import sys

from werkzeug.wsgi import ClosingIterator


class Middleware(object):

    def __init__(self, application, client, detector,
                 before_intercept=None, after_intercept=None):
        #
        self.application = application
        self.client = client
        self.detector = detector
        self.before_intercept = before_intercept
        self.after_intercept = after_intercept
        pass

    def __call__(self, environ, start_response):

        def start_interception(status, response_headers, exc_info=None):

            print("middleware:", "start interception")
            start_response(status, response_headers, exc_info)

            # interception
            raw_current_url = self.detector.detect(environ)
            if not raw_current_url:
                print("middleware:", "no need to intercept")
                return output

            # prepare response
            response = self.client.request(raw_current_url)
            if not isinstance(response, dict):
                print("middleware", "invalid interceptor response")
                return output

            # override write
            print("middleware", "sending interceptor response")

            def write(s):
                print(s)
                return output(bytes(json.dumps(response)))

            return writer

        return ClosingIterator(self.application(environ, start_interception))

    pass
