import docker
from jinja2 import Environment, FileSystemLoader

# Create a new Dockerfile to build on the input image
def create_package_dockerfile(docker_image, package_command):
    env = Environment(
        loader=FileSystemLoader("./"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("Dockerfile_template.j2")
    value = {"docker_image": docker_image, "package_command": "RUN " + package_command}
    with open("Dockerfile", "w") as f:
        f.write(template.render(value))


def create_pip_dockerfile(docker_image, package_command, pip_command):
    env = Environment(
        loader=FileSystemLoader("./"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("Dockerfile_template.j2")
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
    template = env.get_template("Dockerfile_template.j2")
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