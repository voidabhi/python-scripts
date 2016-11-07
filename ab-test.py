#!/usr/bin/env python

import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.escape
import logging
import random

from tornado.options import define, options


define('port', default=8888, help='run on the given port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
        ]

        settings = dict(
            cookie_secret='11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo='
        )

        tornado.web.Application.__init__(self, handlers, **settings)


class ABTestMixin(object):
    __original_ab_tests = {}
    __ab_tests = {}
    __ab_test_cookie_name = 'ab_test'

    def register_ab_tests(self, tests):
        self.__original_ab_tests = tests
        self.__ab_tests = dict({name: value[random.randint(0, 1)] \
                             for name, value in tests.iteritems()},
                             **self.__get_ab_tests())

        if len(self.__ab_tests) > 0:
            self.set_secure_cookie(
                self.__ab_test_cookie_name,
                tornado.escape.json_encode(self.__ab_tests))

    def ab_test(self, name):
        if not self.__ab_tests:
            raise tornado.web.HTTPError(500, 'No registered AB tests')

        try:
            return self.__ab_tests[name]
        except KeyError:
            logging.error('No AB test with name %r', name)

    def is_a_test(self, name):
        return self.ab_test(name) == self.__original_ab_tests[name][0]

    def is_b_test(self, name):
        return not self.is_a_test(name)

    def __get_ab_tests(self):
        cookie = self.get_secure_cookie(self.__ab_test_cookie_name)
        return tornado.escape.json_decode(cookie) if cookie else {}


class MainHandler(tornado.web.RequestHandler, ABTestMixin):
    def prepare(self):
        self.register_ab_tests(dict(
            homepage_design=('original', 'redesign'),
            sign_in_redirection=('to_home', 'to_profile')
        ))

    def get(self):
        logging.info(self.ab_test('homepage_design'))
        logging.info(self.is_b_test('homepage_design'))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
