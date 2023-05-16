import argparse
import json
import subprocess

parser = argparse.ArgumentParser(prog='emileo', description="Scans the given container and attempts to fix vulnerabilities", epilog="Creator: Shane Mulcair")
parser.add_argument('container', help="The container to scan")
args=parser.parse_args()
result = subprocess.run(['./grype', args.container, '--only-fixed', '-o', 'json'], stdout=subprocess.PIPE)
json_report = json.loads(result.stdout)

for match in json_report['matches']:
    print(match['vulnerability'])

