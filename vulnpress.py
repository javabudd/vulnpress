import argparse
from exploits.exploitsql import ExploitSql
from exploits.exploitshell import ExploitShell
from exploits.exploitxss import ExploitXSS
from exploits.sql import *
from exploits.shell import *
from exploits.xss import *

parser = argparse.ArgumentParser()
parser.add_argument('hostname', help='URL')
parser.add_argument('category', help='sql, shell, xss')
args = parser.parse_args()

if args.hostname and args.category:
	print('\r\n')
	hostname = args.hostname
	category = args.category
	if category == 'sql':
		[cls(hostname).exploit() for cls in vars()['ExploitSql'].__subclasses__()]
	if category == 'shell':
		[cls(hostname).exploit() for cls in vars()['ExploitShell'].__subclasses__()]
	if category == 'xss':
		[cls(hostname).exploit() for cls in vars()['ExploitXSS'].__subclasses__()]