# import tornado
import logging
import time

from tornado import ioloop
from tornado.web import RequestHandler, Application
import tornado.ioloop
import tornado.options
import tornado.wsgi
import datetime
import requests
import os

REMOTESERVER = '127.0.0.1:9999'

class BaseRequest(RequestHandler):
    def data_received(self, chunk):
        pass

    def wait_period(self):
        pass

    def get(self, *args, **kwargs):
        print('[{0}] Receive Request ({1})'.format(datetime.datetime.now(), self.__class__.__name__))
        self.wait_period()
        self.write('Request Complete')
        print('[{0}] Serve Request ({1})'.format(datetime.datetime.now(), self.__class__.__name__))


class ThirtySecondSecondRequest(BaseRequest):
    def wait_period(self):
        time.sleep(30)


class TwentySecondSecondRequest(BaseRequest):
    def wait_period(self):
        time.sleep(20)


class TenSecondSecondRequest(BaseRequest):
    def wait_period(self):
        time.sleep(10)


class OneSecondSecondRequest(BaseRequest):
    def wait_period(self):
        time.sleep(1)


class BaseRemoteServer(RequestHandler):
    url=''

    def get(self, *args, **kwargs):
        print('[{0}] Receive Remote Request ({1})'.format(datetime.datetime.now(), self.__class__.__name__))
        self.write(requests.get(self.url.format(REMOTESERVER)).content)
        print('[{0}] Serve Remote Request ({1})'.format(datetime.datetime.now(), self.__class__.__name__))


class RemoteTwentySecondSecondRequest(BaseRemoteServer):
    url = 'http://{0}/20'.format(REMOTESERVER)


class RemoteTenSecondSecondRequest(BaseRemoteServer):
    url = 'http://{0}/10'.format(REMOTESERVER)


class RemoteOneSecondSecondRequest(BaseRemoteServer):
    url = 'http://{0}/1'.format(REMOTESERVER)


def generate_application():
    return Application([
        (r"/remote/1$", RemoteOneSecondSecondRequest),  # Contacts a remote server and returns about 1 second later.
        (r"/remote/10$", RemoteTenSecondSecondRequest),  # Contacts a remote server and returns about 10 seconds later.
        (r"/remote/20$", RemoteTwentySecondSecondRequest),  # Contacts a remote server and returns about 20 seconds later.
        (r"/$", OneSecondSecondRequest),  # Waits 1 second and then returns some text.
        (r"/1$", OneSecondSecondRequest),  # Waits 1 second and then returns some text.
        (r"/10$", TenSecondSecondRequest),  # Waits 10 seconds and then returns some text.
        (r"/20$", TwentySecondSecondRequest),  # Waits 20 seconds and then returns some text.
        (r"/30$", ThirtySecondSecondRequest),  # Waits 30 seconds and then returns some text.


    ], DEBUG=True)


app = generate_application()

if __name__ == "__main__":
    generate_application().listen(int(os.environ.get('PORT')))
    print("Listening on {0}".format(os.environ.get('PORT')))
    tornado.ioloop.IOLoop.current().start()
