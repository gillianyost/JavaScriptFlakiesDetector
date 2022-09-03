while IFS= read -r package
do
  read -r link
  docker run -dit --name flakyDetector -v $(pwd):/home/projects node:lts-fermium-stress 
  docker exec flakyDetector /bin/bash -c 'cd /home/projects; npm install -g jest @jest/test-sequencer; export NODE_PATH=$(npm root --quiet -g); export CI=true;'
  docker exec -w /home/projects flakyDetector /bin/bash -c "./runFlakyDectector.sh $package $link"
  docker stop flakyDetector
  docker rm flakyDetector
done < $1