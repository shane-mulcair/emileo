import argparse
import json
import subprocess
import docker
from jinja2 import Environment, FileSystemLoader

import discover_os

def create_dockerfile(docker_image):
    env = Environment(loader = FileSystemLoader('./'),   trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('Dockerfile.j2')
    value = {"docker_image": docker_image, "package_command": "yum update -y"}
    with open("Dockerfile", "w") as f:
        f.write(template.render(value))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='emileo', description="Scans the given container and attempts to fix vulnerabilities", epilog="Creator: Shane Mulcair")
    parser.add_argument('container', help="The container to scan")
    args=parser.parse_args()
    # result = subprocess.run(['./grype', args.container, '--only-fixed', '-o', 'json'], stdout=subprocess.PIPE)
    # json_report = json.loads(result.stdout)

    # for match in json_report['matches']:
        # print(match['vulnerability'])
    print(discover_os.discover_os(args.container))
    create_dockerfile(args.container)