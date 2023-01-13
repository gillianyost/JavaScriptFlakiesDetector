date '+%d.%b.%Y %T'
docker build . -t flakie_test_image
while IFS="," read -r package link commitNum date testCommand update
do
  echo "$package"
  docker run -dit --cpus 2 -m 8GB --name flakyDetector -v $(pwd):/home/projects flakie_test_image:latest
  docker exec flakyDetector /bin/bash -x -c "/home/projects/runFlakyDectector.sh $package $link $commitNum $3 $2 \"$testCommand\" $update"
  docker stop flakyDetector
  docker rm flakyDetector
  echo "Container Removed"
done < $1
date '+%d.%b.%Y %T'