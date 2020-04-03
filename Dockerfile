FROM ubuntu:latest

WORKDIR /app

RUN apt-get update
RUN apt-get install curl -y

RUN apt-get install gnupg2 -y
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
# update Node version
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list


# Install Pyenv for testing multiple Python versions
RUN DEBIAN_FRONTEND=noninteractive apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
	libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
	xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

# Install some other deps
RUN apt install graphviz python3-distutils -y

# Install Yarn, pip, Protobuf, npm
#RUN apt install npm protobuf-compiler libgconf-2-4 -y
#RUN npm install --global yarn
#RUN npm install --global npm@latest
RUN apt install npm protobuf-compiler libgconf-2-4 -y
RUN npm install npm@latest -g
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt install nodejs -y
RUN npm -v

# (libgconf is for our e2e tests in Cypress)


RUN apt-get update && apt-get install -y python python-dev python3.7 python3.7-dev python3-pip virtualenv libssl-dev libpq-dev git build-essential libfontconfig1 libfontconfig1-dev
RUN pip3 install setuptools pip --upgrade --force-reinstall

RUN pip3 install pipenv

RUN mkdir /app/streamlit


COPY e2e /app/streamlit/e2e
COPY examples /app/streamlit/examples
COPY lib /app/streamlit/lib
COPY Makefile /app/streamlit/Makefile
COPY proto /app/streamlit/proto
COPY scripts /app/streamlit/scripts
COPY docs /app/streamlit/docs
COPY e2e_flaky /app/streamlit/e2e_flaky
COPY frontend /app/streamlit/frontend

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN npm install -g yarn
# Set up pipenv and run make
RUN pip3 install mypy-protobuf
RUN cd /app/streamlit/lib && pipenv --three
RUN cd /app/streamlit && pipenv run make all-devel

RUN cd /app/streamlit/frontend && yarn upgrade
