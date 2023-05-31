FROM cytopia/dvwa:latest

RUN apt-get update && apt-get upgrade -y && apt-get clean all

