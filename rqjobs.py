



import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.gen
import redis
import tornado.options
from rq import Queue

r = redis.Redis()

def test(interval):
    for i in xrange(int(interval)):
        print i
        time.sleep(1)

        return interval

@tornado.gen.coroutine
def get_result(job):
    while True:
        yield tornado.gen.sleep(0.1)
        if job.result is not None or job.status == 'failed':
            break
    raise tornado.gen.Return(job)


class IndexHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, interval=10):

        q = Queue(connection=r)

        job = q.enqueue(test)
        job = yield get_result(job)

        self.write(str(job.result))


if __name__ == '__main__':
    tornado.options.parse_command_line()
    application = tornado.web.Application(handlers=[
        (r"/(\d+)", IndexHandler)
    ], debug=True)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8881)

    tornado.ioloop.IOLoop.instance().start()
