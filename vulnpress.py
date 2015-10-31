import tornado.ioloop
import tornado.web
from db.db import Db
from exploit.exploit import Exploit


class Vulnpress:
    def __init__(self, hostname, protocol, username=None, password=None):
        self.exploiter = Exploit(hostname, protocol, username, password)
        self.exploits = {
            'all': self.exploiter.exploit(),
            'sql': self.exploiter.exploit(4),
            'xss': self.exploiter.exploit(5),
            'shell': self.exploiter.exploit(3),
            'afd': self.exploiter.exploit(1)
        }

    def exploit(self, category):
        return self.exploits.get(category)


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('main.html')

    def post(self, *args, **kwargs):
        category = self.get_argument('exploit_type', None)
        results = None
        if category is not None:
            vp = Vulnpress(self.format_hostname(self.get_argument('hostname', None)),
                           self.get_argument('protocol', 'http://'), self.get_argument('username', None),
                           self.get_argument('password', None))
            results = vp.exploit(category)

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


class Init(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/exploit", ExploitHandler)
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
