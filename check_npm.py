import docker

npm_update_command = "npm update -g"

    
def check_npm(docker_image):
    client=docker.from_env()
    try:
        client.containers.run(docker_image, "npm -v").decode('utf-8')
        client.containers.run(docker_image, "npm outdated").decode('utf-8')
        return npm_update_command
                    
    except:
        print("NPM doesn't seem to be installed")
        return ""
