import tornado.ioloop
import tornado.web
from exploits.exploit import Exploit
from exploits.exploitsql import ExploitSql
from exploits.exploitshell import ExploitShell
from exploits.exploitxss import ExploitXSS
from exploits.exploitescalation import ExploitEscalation
from exploits.exploitafd import ExploitAfd
from exploits.sql import *
from exploits.shell import *
from exploits.xss import *
from exploits.escalation import *
from exploits.afd import *


class Vulnpress:
	def __init__(self, hostname, username=None, password=None):
		self.hostname = hostname
		self.formathostname()
		self.isloggedin = self.login(username, password)

	def exploit(self, category):
		self.EXPLOITS.get(category)(self)

		return Exploit.exploits

	def login(self, username, password):
		isloggedin = False
		if username is not None and password is not None:
			isloggedin = Exploit().login(self.hostname, username, password)
			if isloggedin is False or isloggedin is None:
				exit("\n"'Unable to login with those credentials')
		return isloggedin

	def formathostname(self):
		if self.hostname[:8] == 'https://':
			# ssl not supported yet
			return False
		if self.hostname[:7] != "http://":
			self.hostname = 'http://' + self.hostname

	def exploitall(self):
		self.exploitsql()
		self.exploitshell()
		self.exploitescalation()
		self.exploitxss()
		self.exploitafd()

	def exploitsql(self):
		[cls(self.hostname, self.isloggedin).exploit() for cls in ExploitSql.__subclasses__()]

	def exploitxss(self):
		[cls(self.hostname, self.isloggedin).exploit() for cls in ExploitXSS.__subclasses__()]

	def exploitescalation(self):
		[cls(self.hostname, self.isloggedin).exploit() for cls in ExploitEscalation.__subclasses__()]

	def exploitshell(self):
		[cls(self.hostname, self.isloggedin).exploit() for cls in ExploitShell.__subclasses__()]

	def exploitafd(self):
		[cls(self.hostname, self.isloggedin).exploit() for cls in ExploitAfd.__subclasses__()]

	EXPLOITS = {
		'all': exploitall,
		'sql': exploitsql,
		'xss': exploitxss,
		'escalation': exploitescalation,
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
	init = Init()

	init.listen(8888, address='localhost')
	tornado.ioloop.IOLoop.current().start()
