import argparse
from colorama import Fore, Style, init
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

init()
parser = argparse.ArgumentParser()
scangroup = parser.add_argument_group('Scan', 'Scan arguments')
logingroup = parser.add_argument_group('Login', 'Wordpress login options')
scangroup.add_argument('hostname', help='server hostname')
scangroup.add_argument('category', help='afd(arbitrary file download), escalation(privilege escalation), shell(shell upload), sql(sql injection), xss(cross site scripting)', choices=['all', 'afd', 'escalation', 'shell', 'sql', 'xss'])
logingroup.add_argument('--username', help='Optional Wordpress username')
logingroup.add_argument('--password', help='Optional Wordpress password')

args = parser.parse_args()


class Vulnpress():
	def __init__(self, hostname, category, username, password):
		self.hostname = self.formathostname(hostname)
		self.loggedin = self.login(username, password)
		self.exploit(category)

	def exploit(self, category):
		self.EXPLOITS.get(category)(self)

	def login(self, username, password):
		loggedin = False
		if username and password:
			loggedin = Exploit().login(self.hostname, username, password)
			if loggedin is False or loggedin is None:
				exit("\n" + Fore.RED + 'Unable to login with those credentials' + Style.RESET_ALL)
		return loggedin

	@staticmethod
	def formathostname(hostname):
		if hostname[:8] == 'https://':
			return
		if hostname[:7] != "http://":
			return 'http://' + hostname

	def exploitall(self):
		self.exploitsql()
		self.exploitshell()
		self.exploitescalation()
		self.exploitxss()
		self.exploitafd()

	def exploitsql(self):
		print("\n" + Fore.CYAN + 'Running SQL exploits...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitSql.__subclasses__()]

	def exploitxss(self):
		print("\n" + Fore.CYAN + 'Running XSS exploits...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitXSS.__subclasses__()]

	def exploitescalation(self):
		print("\n" + Fore.CYAN + 'Running privilege escalation exploits...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitEscalation.__subclasses__()]

	def exploitshell(self):
		print("\n" + Fore.CYAN + 'Running shell upload exploits...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitShell.__subclasses__()]

	def exploitafd(self):
		print("\n" + Fore.CYAN + 'Running arbitrary file download exploits...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitAfd.__subclasses__()]

	EXPLOITS = {
		'all': exploitall,
		'sql': exploitsql,
		'xss': exploitxss,
		'escalation': exploitescalation,
		'shell': exploitshell,
		'afd': exploitafd
	}

Vulnpress(args.hostname, args.category, args.username, args.password)
