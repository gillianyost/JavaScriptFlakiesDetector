#!/bin/bash
while IFS= read -r package
do
  sudo docker run -dit --name flakyDetector -v $(pwd):/home/project node:lts-fermium
  sudo docker exec flakyDetector /bin/bash -c 'cd /home/project; npm install seedrandom; npm install -g jest @jest/test-sequencer; export NODE_PATH=$(npm root --quiet -g); export CI=true;'
  sudo docker exec -w /home/project flakyDetector /bin/bash -c "./inner.sh $package"
  sudo docker stop flakyDetector
  sudo docker rm flakyDetector
done < $1