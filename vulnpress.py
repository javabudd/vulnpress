import argparse
from exploits import exploitsql
from exploits import exploitshell

parser = argparse.ArgumentParser()
parser.add_argument('hostname', help='URL')
parser.add_argument('category', help='sql, shell')
args = parser.parse_args()

if args.hostname and args.category:
	hostname = args.hostname
	category = args.category
	if category == 'sql':
		exploitsql.ExploitSql(hostname)
	if category == 'shell':
		exploitshell.ExploitShell(hostname)