import docker
import logging

npm_update_command = "npm update -g"

def read_blocklist():
    with open('npm_blocklist.txt', 'r') as f:
        return f.read().splitlines()
    
def check_npm(docker_image):
    client=docker.from_env()
    try:
        client.containers.run(docker_image, "npm -v").decode('utf-8')
        npm_vuln_list = client.containers.run(docker_image, "npm outdated").decode('utf-8').decode('utf-8')
        package_list = []
        for p in npm_vuln_list.split('\n'):
            if p != '':
                package_list.append(p.split(' ')[0])
        return package_list
        
    except:
        logging.error("NPM doesn't seem to be installed")
        return []

def update_npm_packages(package_list):
    allowlist = read_blocklist()
    update_command = npm_update_command
    for package in package_list:
        if package not in allowlist:
            update_command = update_command + str(package) + " "
    logging.info(update_command)
    if update_command != npm_update_command:
        return update_command
    else:
        return ""
