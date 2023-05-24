import docker

pip_update_command = "pip3 install --upgrade "

def read_allowlist():
    with open('pip_allowlist.txt', 'r') as f:
        return f.read().splitlines()
    
def check_pip_packages(docker_image):
    client=docker.from_env()
    try:
        pip_vuln_list = client.containers.run(docker_image, "pip3 list --outdated").decode('utf-8')
        package_list = []
        for p in pip_vuln_list.split('\n'):
            if p != '':
                package_list.append(p.split(' ')[0])
        return package_list
            
    except:
        print("Pip doesn't seem to be installed")
        return []
    
def update_pip_packages(docker_image, package_list):
    allowlist = read_allowlist()
    update_command = pip_update_command
    for package in package_list:
        if package not in allowlist:
            update_command = update_command + package + " "
    print(update_command)
    if update_command != pip_update_command:
        return update_command
    else:
        return ""
