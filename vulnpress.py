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
scangroup.add_argument('category', help='all, sql, shell, xss', choices=['all', 'escalation', 'shell', 'sql', 'xss'])
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
		print("\n" + Fore.GREEN + 'Running all exploits...' + Style.RESET_ALL + "\n")
		print("\n" + Fore.GREEN + 'SQL...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitSql.__subclasses__()]
		print("\n" + Fore.GREEN + 'XSS...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitXSS.__subclasses__()]
		print("\n" + Fore.GREEN + 'Shell upload...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitShell.__subclasses__()]
		print("\n" + Fore.GREEN + 'Privilege escalation...' + Style.RESET_ALL + "\n")

	def exploitsql(self):
		print("\n" + Fore.GREEN + 'Running SQL exploits...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitSql.__subclasses__()]

	def exploitxss(self):
		print("\n" + Fore.GREEN + 'Running XSS exploits...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitXSS.__subclasses__()]

	def exploitescalation(self):
		print("\n" + Fore.GREEN + 'Running privilege escalation exploits...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitEscalation.__subclasses__()]

	def exploitshell(self):
		print("\n" + Fore.GREEN + 'Running shell upload exploits...' + Style.RESET_ALL + "\n")
		[cls(self.hostname, self.loggedin).exploit() for cls in ExploitShell.__subclasses__()]

	EXPLOITS = {
		'all': exploitall,
		'sql': exploitsql,
		'xss': exploitxss,
		'escalation': exploitescalation,
		'shell': exploitshell
	}

Vulnpress(args.hostname, args.category, args.username, args.password)
