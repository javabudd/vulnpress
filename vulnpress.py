import tornado.ioloop
import tornado.web
from db.db import Db
from exploit.exploit import Exploit


class Vulnpress:
    def __init__(self, hostname, username=None, password=None):
        self.exploiter = Exploit(hostname, username, password)

    def exploit(self, category):
        return self.EXPLOITS.get(category)(self)

    def exploitall(self):
        return self.exploiter.exploit()

    def exploitsql(self):
        return self.exploiter.exploit(4)

    def exploitxss(self):
        return self.exploiter.exploit(5)

    def exploitshell(self):
        return self.exploiter.exploit(3)

    def exploitafd(self):
        return self.exploiter.exploit(1)

    EXPLOITS = {
        'all': exploitall,
        'sql': exploitsql,
        'xss': exploitxss,
        'shell': exploitshell,
        'afd': exploitafd
    }


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('main.html')

    def post(self, *args, **kwargs):
        category = self.get_argument('exploit_type', None)
        results = None
        if category is not None:
            vp = Vulnpress(self.get_argument('hostname', None), self.get_argument('username', None),
                           self.get_argument('password', None))
            results = vp.exploit(category)

        self.write(results)


class ExploitHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        exploit = Db().get_exploit_by_id(self.get_argument('id'))
        self.render('exploit.html', exploit=exploit, type=Db().get_exploit_type_by_id(exploit.type_id))

    def post(self, *args, **kwargs):
        category = self.get_argument('exploit_type', None)
        results = None
        if category is not None:
            vp = Vulnpress(self.get_argument('hostname', None), self.get_argument('username', None),
                           self.get_argument('password', None))
            results = vp.exploit(category)

        self.write(results)


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
