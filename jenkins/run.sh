#!/bin/bash

set -e

docker run -p 8080:8080 -p 50000:50000 --restart=on-failure -v /home/shane/Desktop/masters/jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock jenkins_with_docker