import argparse
import json
import subprocess
import docker
from jinja2 import Environment, FileSystemLoader

import check_pip
import discover_os

# Create a new Dockerfile to build on the input image
def create_package_dockerfile(docker_image, package_command):
    env = Environment(
        loader=FileSystemLoader("./"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("Dockerfile.j2")
    value = {"docker_image": docker_image, "package_command": "RUN " + package_command}
    with open("Dockerfile", "w") as f:
        f.write(template.render(value))

def create_pip_dockerfile(docker_image, package_command, pip_command):
    env = Environment(
        loader=FileSystemLoader("./"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("Dockerfile.j2")
    value = {"docker_image": docker_image, "package_command": "RUN " + package_command, "pip_command": "RUN " + pip_command}
    with open("Dockerfile", "w") as f:
        f.write(template.render(value))

# Build the new container with the update commands
def rebuild_container(docker_image):
    client = docker.from_env()
    client.images.build(path=".", tag=docker_image + "_updated")

# Scan with the local grype build
def scan_with_grype(docker_image):
    result = subprocess.run(
        ["./grype", docker_image, "--only-fixed", "-o", "json"], stdout=subprocess.PIPE
    )
    json_report = json.loads(result.stdout)

    print("Number of vulnerabilities found: " + str(len(json_report["matches"])))
    return len(json_report["matches"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="emileo",
        description="Scans the given container and attempts to fix vulnerabilities",
        epilog="Creator: Shane Mulcair",
    )
    parser.add_argument("container", help="The container to scan")
    args = parser.parse_args()
    
    num_fixable_vulns = scan_with_grype(args.container)
    package_cmd = ""
    if num_fixable_vulns > 0:
        package_cmd = discover_os.discover_os(args.container)
        create_package_dockerfile(args.container, package_cmd)
        rebuild_container(args.container)
        scan_with_grype(args.container + "_updated")

    pip_vulns = check_pip.check_pip_packages(args.container)
    if len(pip_vulns) > 0:
        print(pip_vulns)
    pip_update_command = check_pip.update_pip_packages(args.container, pip_vulns)
    if pip_update_command != "":
        create_pip_dockerfile(args.container, package_cmd, pip_update_command)
        rebuild_container(args.container)
        scan_with_grype(args.container + "_updated")

