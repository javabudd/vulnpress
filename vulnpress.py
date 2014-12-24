import argparse
from colorama import Fore, Style, init
from exploits.base import Base
from exploits.exploitsql import ExploitSql
from exploits.exploitshell import ExploitShell
from exploits.exploitxss import ExploitXSS
from exploits.sql import *
from exploits.shell import *
from exploits.xss import *

init()
parser = argparse.ArgumentParser()
scangroup = parser.add_argument_group('Scan', 'Scan arguments')
logingroup = parser.add_argument_group('Login', 'Wordpress login options')
scangroup.add_argument('hostname', help='server hostname')
scangroup.add_argument('category', help='sql, shell, xss', choices=['sql', 'shell', 'xss'])
scangroup.add_argument('--secure', action='store_true', help='HTTPS')
logingroup.add_argument('-u', help='Optional Wordpress username')
logingroup.add_argument('-p', help='Optional Wordpress password')

args = parser.parse_args()


class Vulnpress():
	def __init__(self, hostname, category, username=None, password=None):
		self.hostname = hostname
		self.category = category
		self.username = username
		self.password = password
		self.init()

	def init(self):
		login = False
		https = False
		if self.username and self.password:
			login = True
		if args.secure:
			# https = True
			print(Fore.RED + '\nHTTPS not currently supported' + Style.RESET_ALL)
		self.exploitcategory(self.category, login=login, https=https)

	def exploitcategory(self, category, login=False, https=False):
		if not https:
			self.formathostname()
		else:
			self.formathostname(True)
		loggedin = False
		if login:
			loggedin = Base().login(self.hostname, self.username, self.password)
		if category == 'sql':
			[cls(self.hostname, loggedin).exploit() for cls in ExploitSql.__subclasses__()]
		if category == 'xss':
			[cls(self.hostname, loggedin).exploit() for cls in ExploitXSS.__subclasses__()]
		if category == 'shell':
			[cls(self.hostname, loggedin).exploit() for cls in ExploitShell.__subclasses__()]

	def formathostname(self, https=False):
		if self.hostname[:7] != "http://":
					self.hostname = 'http://' + self.hostname
		if https:
			if self.hostname[:7] != "https://":
					self.hostname = 'https://' + self.hostname

Vulnpress(args.hostname, args.category, args.u, args.p)