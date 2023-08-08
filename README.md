# emileo

A python tool to wrap the Grype vulnerability scanner. The concept is to run Grype, and if there are fixable vulnerabilities reported against a container, emileo will identify the container OS, and add some new layers onto the container applying package manager, python and npm updates.

## Installation

Install the latest version of Grype from https://github.com/anchore/grype/releases

Install the pip dependencies with `pip3 install --user -r requirements.txt`

## Running

```./run.py -h 
usage: emileo [-h] --container CONTAINER [--scan_only SCAN_ONLY] [--show_not_fixable SHOW_NOT_FIXABLE] [--os_updates] [--pip_updates] [--npm_updates]
              [--defect_dojo]

Scans the given container and attempts to fix vulnerabilities

options:
  -h, --help            show this help message and exit
  --container CONTAINER
                        The container to scan
  --scan_only SCAN_ONLY
                        Only scan for issues, don't try to fix
  --show_not_fixable SHOW_NOT_FIXABLE
                        List the packages that don't have a fix available
  --os_updates          Figure out the package manager and apply OS upates
  --pip_updates         Update any needed pip packages, if found
  --npm_updates         See if npm is installed and do a global package update
  --defect_dojo         Upload all results to defect Dojo

Creator: Shane Mulcair```

