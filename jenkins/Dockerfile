FROM jenkins/jenkins:lts-jdk11

ENV CASC_JENKINS_CONFIG /var/casc_config
ENV JAVA_OPTS=-Djenkins.install.runSetupWizard=false

USER root

RUN apt-get update && \
    apt-get -y install apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    wget \
    software-properties-common && \
    curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg > /tmp/dkey; apt-key add /tmp/dkey && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
    $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get -y install docker-ce glibc-source && \
    wget https://github.com/anchore/grype/releases/download/v0.62.3/grype_0.62.3_linux_amd64.deb && dpkg -i grype_0.62.3_linux_amd64.deb && \
    apt-get install -y python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install docker jinja2 && \
    mkdir -p /var/casc_config

# Automated plugin install from plugins.txt
COPY --chown=jenkins:jenkins plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

COPY --chown=jenkins:jenkins config.yaml /var/casc_config

# Drop back to the regular jenkins user - good practice
USER jenkins