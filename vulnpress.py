import argparse
from colorama import Fore, Style, init
from exploits.exploit import Exploit
from exploits.exploitsql import ExploitSql
from exploits.exploitshell import ExploitShell
from exploits.exploitxss import ExploitXSS
from exploits.exploitescalation import ExploitEscalation
from exploits.sql import *
from exploits.shell import *
from exploits.xss import *
from exploits.escalation import *

init()
parser = argparse.ArgumentParser()
scangroup = parser.add_argument_group('Scan', 'Scan arguments')
logingroup = parser.add_argument_group('Login', 'Wordpress login options')
scangroup.add_argument('hostname', help='server hostname')
scangroup.add_argument('category', help='all, sql, shell, xss', choices=['all', 'sql', 'shell', 'xss'])
logingroup.add_argument('--username', help='Optional Wordpress username')
logingroup.add_argument('--password', help='Optional Wordpress password')

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
		if self.username and self.password:
			login = True
		self.formathostname()
		self.exploitcategory(self.category, login=login)

	def exploitcategory(self, category, login=False):
		loggedin = False
		if login:
			loggedin = Exploit().login(self.hostname, self.username, self.password)
			if loggedin is False or loggedin is None:
				exit("\n" + Fore.RED + 'Unable to login with those credentials' + Style.RESET_ALL)
		if category == 'all':
			print("\n" + Fore.GREEN + 'Running all exploits...' + Style.RESET_ALL + "\n")
			print("\n" + Fore.GREEN + 'SQL...' + Style.RESET_ALL + "\n")
			[cls(self.hostname, loggedin).exploit() for cls in ExploitSql.__subclasses__()]
			print("\n" + Fore.GREEN + 'XSS...' + Style.RESET_ALL + "\n")
			[cls(self.hostname, loggedin).exploit() for cls in ExploitXSS.__subclasses__()]
			print("\n" + Fore.GREEN + 'Shell upload...' + Style.RESET_ALL + "\n")
			[cls(self.hostname, loggedin).exploit() for cls in ExploitShell.__subclasses__()]
			print("\n" + Fore.GREEN + 'Privilege escalation...' + Style.RESET_ALL + "\n")
		elif category == 'sql':
			print("\n" + Fore.GREEN + 'Running all SQL exploits...' + Style.RESET_ALL + "\n")
			[cls(self.hostname, loggedin).exploit() for cls in ExploitSql.__subclasses__()]
		elif category == 'xss':
			print("\n" + Fore.GREEN + 'Running all XSS exploits...' + Style.RESET_ALL + "\n")
			[cls(self.hostname, loggedin).exploit() for cls in ExploitXSS.__subclasses__()]
		elif category == 'shell':
			print("\n" + Fore.GREEN + 'Running all shell upload exploits...' + Style.RESET_ALL + "\n")
			[cls(self.hostname, loggedin).exploit() for cls in ExploitShell.__subclasses__()]
		elif category == 'escalation':
			print("\n" + Fore.GREEN + 'Running all privilege escalation exploits...' + Style.RESET_ALL + "\n")
			[cls(self.hostname, loggedin).exploit() for cls in ExploitEscalation.__subclasses__()]

	def formathostname(self):
		if self.hostname[:8] == 'https://':
			return
		if self.hostname[:7] != "http://":
			self.hostname = 'http://' + self.hostname

Vulnpress(args.hostname, args.category, args.username, args.password)
