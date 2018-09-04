FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY ./requirements.txt /tmp/r.txt
RUN pip install -r /tmp/r.txt

EXPOSE 5000
