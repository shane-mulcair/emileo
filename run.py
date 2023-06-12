import argparse
import json
import subprocess
import docker
from jinja2 import Environment, FileSystemLoader

import check_npm
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
    value = {
        "docker_image": docker_image,
        "package_command": "RUN " + package_command,
        "pip_command": "RUN " + pip_command,
    }
    with open("Dockerfile", "w") as f:
        f.write(template.render(value))

def create_npm_dockerfile(docker_image, package_command, pip_command, npm_command):
    env = Environment(
        loader=FileSystemLoader("./"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("Dockerfile.j2")
    value = {
        "docker_image": docker_image,
        "package_command": "RUN " + package_command,
        "pip_command": "RUN " + pip_command,
        "npm_command": "RUN " + npm_command,
    }
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
    parser.add_argument("--container", help="The container to scan")
    parser.add_argument("--scan_only", help="Only scan for issues, don't try to fix")
    parser.add_argument("--show_not_fixable", help="List the packages that don't have a fix available")
    parser.add_argument("--os_updates", help="Figure out the package manager and apply OS upates")
    parser.add_argument("--pip_updates", help="Update any needed pip packages, if found")
    parser.add_argument("--npm_updates", help="See if npm is installed and do a global package update")
    args = parser.parse_args()
    container_name = args.container

    print("Initial scan using Grype")
    num_fixable_vulns = scan_with_grype(container_name)
    package_cmd = ""
    if num_fixable_vulns > 0:
        print("There are fixable vulnerabilities - discovering the package manager now")
        package_cmd = discover_os.discover_os(container_name)
        create_package_dockerfile(container_name, package_cmd)
        print("Rebuilding the container with package manager updates")
        rebuild_container(container_name)

        scan_with_grype(container_name + "_updated")

    container_name = container_name + "_updated"
    print("Checking if pip is installed for pyton packages")
    pip_vulns = check_pip.check_pip_packages(container_name)
    pip_update_command = ""
    if len(pip_vulns) > 0:
        pip_update_command = check_pip.update_pip_packages(container_name, pip_vulns)
        if pip_update_command != "":
            create_pip_dockerfile(container_name, package_cmd, pip_update_command)
            print("Rebuilding the container with pip updates")
            rebuild_container(container_name)
            scan_with_grype(container_name)

    npm_update_command = check_npm.check_npm(container_name)
    if npm_update_command != "":
        create_npm_dockerfile(container_name, package_cmd, pip_update_command, npm_update_command)
        print("Rebuilding the container with npm updates")
        rebuild_container(container_name)
        scan_with_grype(container_name)
