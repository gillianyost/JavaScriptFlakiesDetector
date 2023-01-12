# Pull base node:lts-fermium
FROM node:lts-fermium

MAINTAINER gillianyost

RUN apt-get update && apt-get -y install stress-ng
RUN useradd -ms /bin/bash -c "flakie" flakie && echo "flakie:docker"
RUN npm install -g jest
RUN cd /home/flakie
RUN npm install seedrandom
RUN npm install jest @jest/test-sequencer
RUN cd ~ 
RUN export NODE_PATH=$(npm root --quiet -g) 
RUN export CI=true
