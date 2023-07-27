import docker

commands = {"/etc/redhat-release": "yum update -y && yum clean all",
            "/etc/arch-release": "pacman -Syu",
            "/etc/gentoo-release": "emaint -a sync && emerge -uDN @world",
            "/etc/SuSE-release": "zypper up --non-interactive",
            "/etc/debian_version": "apt-get update && apt-get upgrade -y && apt-get clean all",
           "/etc/alpine-release": "apk update && apk upgrade -y && apk clean"
            }

# Figure out which package manager to use
def discover_os(docker_image):
    client=docker.from_env()
    for cmd in commands:
        try:
            result = client.containers.run(docker_image, "cat " + cmd)
            if cmd == "/etc/redhat-release":
                if "release 8" in str(result):
                    return "dnf update -y && dnf clean all"
            return commands[cmd]
        except docker.errors.ContainerError as e:
            continue
    return "No match found"