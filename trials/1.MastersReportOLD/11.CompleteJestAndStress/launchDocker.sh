while IFS="," read -r package link commitNum date testCommand
do
  echo "$package"
  docker run -dit --name flakyDetector -v $(pwd):/home/projects node:lts-fermium-flaky
  # docker exec flakyDetector /bin/bash -c 'cd /home/projects; npm install -g jest @jest/test-sequencer; export NODE_PATH=$(npm root --quiet -g); export CI=true;'
  docker exec -w /home/projects flakyDetector /bin/bash -c "./runFlakyDectector_user.sh $package $link $commitNum --no_stress $2 $testCommand"
  # echo "Sucessful Run of Non-Stress Flaky Detector"
  docker exec -w /home/projects flakyDetector /bin/bash -c "./runFlakyDectector_user.sh $package $link $commitNum --stress $2 $testCommand"
  # echo "Sucessful Run of Stress Flaky Detector"
  docker stop flakyDetector
  docker rm flakyDetector
  echo "Container Removed"
done < $1