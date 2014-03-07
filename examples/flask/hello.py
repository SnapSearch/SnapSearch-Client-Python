from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':

    # load snapsearch credentials
    import os
    credentials = os.environ.get('SNAPSEARCH_API_CREDENTIALS', "")
    api_email, sep, api_key = credentials.partition(":")

    # initialize Client and Detector
    from SnapSearch import Client, Detector
    client = Client(api_email, api_key)
    detector = Detector()

    # hook the middleware
    from wsgi import Middleware
    app.wsgi_app = wsgi.Middleware(app.wsgi_app, client, detector)
    app.run(host="127.0.0.1", port=5000)
