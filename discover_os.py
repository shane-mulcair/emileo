import docker

commands = {"/etc/redhat-release": "yum",
            "/etc/arch-release": "pacman",
            "/etc/gentoo-release": "emerge",
            "/etc/SuSE-release": "zypp",
            "/etc/debian_version": "apt-get",
           "/etc/alpine-release": "apk"
            }
def discover_os(docker_image):
    client=docker.from_env()
    for cmd in commands:
        print(cmd)
        try:
            client.containers.run(docker_image, "cat " + cmd)
            return commands[cmd]
        except docker.errors.ContainerError as e:
            continue
    return "No idea"