#! /usr/bin/python3
import argparse
import json
import logging
import subprocess

import check_npm
import check_pip
import discover_os
import docker_worker
import defect_dojo


# Scan with the local grype build
def scan_with_grype(docker_image, show_not_fixable, use_defect_dojo):
    if show_not_fixable:
        result = subprocess.run(
            ["grype", docker_image, "-o", "json"], stdout=subprocess.PIPE
        )
    else:
        result = subprocess.run(
            ["grype", docker_image, "--only-fixed", "-o", "json"], stdout=subprocess.PIPE
        )
    if result.returncode == 0:
        json_report = json.loads(result.stdout)
        if use_defect_dojo:
            with open('result.json', 'w') as f:
                f.write(json.dumps(json_report))
            if not defect_dojo.check_product_exists(docker_image):
                defect_dojo.create_product(docker_image, "Created via emileo tool")
            defect_dojo.upload_report(docker_image, json_report)
            logging.info("Successfully uploaded to Defect Dojo")
        logging.info("Number of vulnerabilities found: " + str(len(json_report["matches"])))
        return len(json_report["matches"])
    else:
        logging.error("Non-zero return code from grype: " + str(result.returncode))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="emileo",
        description="Scans the given container and attempts to fix vulnerabilities",
        epilog="Creator: Shane Mulcair",
    )
    parser.add_argument("--container", required=True, help="The container to scan")
    parser.add_argument("--scan_only", help="Only scan for issues, don't try to fix")
    parser.add_argument("--show_not_fixable", help="List the packages that don't have a fix available")
    parser.add_argument("--os_updates", action='store_true', default=True, help="Figure out the package manager and apply OS upates")
    parser.add_argument("--pip_updates", action='store_true', default=False, help="Update any needed pip packages, if found")
    parser.add_argument("--npm_updates", action='store_true', default=False, help="See if npm is installed and do a global package update")
    parser.add_argument("--defect_dojo", action='store_true', default=False, help="Upload all results to defect Dojo")
    args = parser.parse_args()
    container_name = args.container

    logging.info("Initial scan using Grype")
    num_fixable_vulns = scan_with_grype(container_name, args.show_not_fixable, args.defect_dojo)
    if args.scan_only:
        logging.info("Only scanning, exiting.")
        exit(0)
    package_cmd = ""
    if args.os_updates:
        if num_fixable_vulns > 0:
            logging.info("There are fixable vulnerabilities - discovering the package manager now")
            package_cmd = discover_os.discover_os(container_name)
            docker_worker.create_package_dockerfile(container_name, package_cmd)
            logging.info("Rebuilding the container with package manager updates")
            docker_worker.rebuild_container(container_name)

            scan_with_grype(container_name + "_updated", args.show_not_fixable, args.defect_dojo)

    container_name = container_name + "_updated"
    if args.pip_updates:
        logging.info("Checking if pip is installed for python packages")
        pip_vulns = check_pip.check_pip_packages(container_name)
        pip_update_command = ""
        if len(pip_vulns) > 0:
            pip_update_command = check_pip.update_pip_packages(container_name, pip_vulns)
            if pip_update_command != "":
                docker_worker.create_pip_dockerfile(container_name, package_cmd, pip_update_command)
                logging.info("Rebuilding the container with pip updates")
                docker_worker.rebuild_container(container_name)
                scan_with_grype(container_name, args.show_not_fixable, args.defect_dojo)

    if args.npm_updates:
        npm_update_command = check_npm.check_npm(container_name)
        if npm_update_command != "":
            docker_worker.create_npm_dockerfile(container_name, package_cmd, pip_update_command, npm_update_command)
            logging.info("Rebuilding the container with npm updates")
            docker_worker.rebuild_container(container_name)
            scan_with_grype(container_name, args.show_not_fixable, args.defect_dojo)
