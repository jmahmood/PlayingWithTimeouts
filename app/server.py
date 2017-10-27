# import tornado
import logging
import time

from tornado.web import RequestHandler, Application
import tornado.ioloop
import tornado.options
import tornado.wsgi
import datetime

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


def generate_application():
    return Application([
        (r"/1", OneSecondSecondRequest),  # Waits 1 second and then returns some text.
        (r"/10", TenSecondSecondRequest),  # Waits 10 seconds and then returns some text.
        (r"/20", TwentySecondSecondRequest),  # Waits 20 seconds and then returns some text.
        (r"/30", ThirtySecondSecondRequest),  # Waits 30 seconds and then returns some text.
    ], DEBUG=True)


app = generate_application()

"""
if __name__ == "__main__":
    tornado.options.define('port', default=2500, help='port we run on', type='int')
    tornado.options.parse_command_line()
    generate_application().listen(int(tornado.options.options.port))
    tornado.ioloop.IOLoop.current().start()
"""