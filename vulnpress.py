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
parser.add_argument('-s', action='store_true', help='HTTPS')
args = parser.parse_args()

hostname = args.hostname
category = args.category

if args.s and hostname and category:
	print('HTTPS not currently supported')

elif hostname and category:
	if hostname[:7] != "http://":
			hostname = 'http://' + hostname
	print('\r\n')
	if category == 'sql':
		[cls(hostname).exploit() for cls in vars()['ExploitSql'].__subclasses__()]
	if category == 'shell':
		[cls(hostname).exploit() for cls in vars()['ExploitShell'].__subclasses__()]
	if category == 'xss':
		[cls(hostname).exploit() for cls in vars()['ExploitXSS'].__subclasses__()]