import tornado.ioloop
import tornado.web
from exploits.exploit import Exploit


class Vulnpress:
    def __init__(self, hostname, username=None, password=None):
        hostname = self.formathostname(hostname)
        self.sploiter = Exploit(hostname, self.login(hostname, username, password))

    def exploit(self, category):
        self.EXPLOITS.get(category)(self)
        exploitjson = Exploit.exploits
        Exploit.exploits = {'found': {}, 'not_found': {}}

        return exploitjson

    def login(self, hostname, username, password):
        isloggedin = False
        if username is not None and password is not None:
            isloggedin = self.sploiter.login(hostname, username, password)
            if isloggedin is False or isloggedin is None:
                exit("\n"'Unable to login with those credentials')
        return isloggedin

    def exploitall(self):
        self.sploiter.exploit()

    def exploitsql(self):
        self.sploiter.exploit_type(4)

        return self

    def exploitxss(self):
        self.sploiter.exploit_type(5)

        return self

    def exploitshell(self):
        self.sploiter.exploit_type(3)

        return self

    def exploitafd(self):
        self.sploiter.exploit_type(1)

        return self

    @staticmethod
    def formathostname(hostname):
        if hostname[:8] == 'https://':
            # ssl not supported yet
            pass
        if hostname[:7] != "http://":
            return 'http://' + hostname

        return hostname

    EXPLOITS = {
        'all': exploitall,
        'sql': exploitsql,
        'xss': exploitxss,
        'shell': exploitshell,
        'afd': exploitafd
    }


class ExploitHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('exploit.html', results=None)

    def post(self, *args, **kwargs):
        category = self.get_argument('exploit_type', None)
        hostname = self.get_argument('hostname', None)
        results = None
        if category is not None:
            vp = Vulnpress(hostname)
            results = vp.exploit(category)

        self.write(results)


class Init(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", ExploitHandler)
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
