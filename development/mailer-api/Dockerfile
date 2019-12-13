FROM ubuntu:18.04

# installing pip with all build dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  python3.7 \
  python3.7-dev \
  python3-pip

RUN python3.7 -m pip install --upgrade \
    pip \
    setuptools \
    wheel \
    ipdb

COPY mailer-api/requirements.txt /usr/src/app/requirements.txt

WORKDIR /usr/src/app/

RUN pip3.7 install -r /usr/src/app/requirements.txt
