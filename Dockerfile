FROM ubuntu:latest

# install packages
RUN apt update
RUN apt install -y python3 python3-pip
RUN pip3 install requests
RUN apt install -y curl

ADD . /root/

# copy script inside container
COPY docker-run.sh /root/
WORKDIR /root
# run when container starts
CMD ["bash", "/root/docker-run.sh"]