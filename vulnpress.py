import tornado.ioloop
import tornado.web
from db.db import Db
from exploit.exploit import Exploit


class Vulnpress:
    def __init__(self, hostname, protocol, username=None, password=None):
        self.exploiter = Exploit(hostname, protocol, username, password)


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('main.html', quote=Db().get_random_quote())

    def post(self, *args, **kwargs):
        exploit_type = self.get_argument('exploit_type')
        results = None
        if exploit_type is not None:
            vp = Vulnpress(self.format_hostname(self.get_argument('hostname', None)),
                           self.get_argument('protocol', 'http://'), self.get_argument('username', None),
                           self.get_argument('password', None))
            if exploit_type == 'all':
                results = vp.exploiter.exploit()
            else:
                results = vp.exploiter.exploit(exploit_type)

        self.write(results)

    @staticmethod
    def format_hostname(hostname):
        if hostname[:7] == "http://":
            hostname = hostname[7:]
        elif hostname[:8] == "https://":
            hostname = hostname[8:]

        if hostname[:4] == "www.":
            hostname = hostname[4:]

        return hostname.strip()


class ExploitHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        exploit = Db().get_exploit_by_id(self.get_argument('id'))
        self.render('exploit.html', exploit=exploit, type=Db().get_exploit_type_by_id(exploit.type_id))


class ExploitsHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        exploits = Db().get_exploits()
        self.render('exploits.html', exploits=exploits)


class Init(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/exploit", ExploitHandler),
            (r"/exploits", ExploitsHandler)
        ]
        settings = {
            'debug': True,
            'template_path': 'web/templates',
            'static_path': "web"
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    Init().listen(8888, address='localhost')
    tornado.ioloop.IOLoop.current().start()
