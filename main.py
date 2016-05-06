#-*- coding:utf-8 -*-
# test url : http://localhost/?id1=2147152072&id2=189831743
from datetime import datetime
import textwrap
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import findPath
from tornado.options import define, options
define("port", default=80, help="run on the given port", type=int)

class IDHandler(tornado.web.RequestHandler):
    def get(self):
        start_time = datetime.now()
        print_result = findPath.getResult(self.get_argument('id1'),self.get_argument('id2'))
        self.write(print_result)
        delta = datetime.now() - start_time
        self.write("\n Cost time: %s ms"%(str(delta.microseconds/1000)))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/$", IDHandler),
        ],
        debug = True
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
