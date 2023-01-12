date '+%d.%b.%Y %T'
docker build . -t flakie_test_image
for i in 1 2 3 4 5 6
do
  while IFS="," read -r package link commitNum date testCommand update
  do
    echo "$package"
    echo UPDATE VAR
    echo "$update"
    docker run -dit --name flakyDetector -v $(pwd):/home/projects flakie_test_image:latest
    echo I
    echo $i
    docker exec flakyDetector /bin/bash -x -c "/home/projects/runFlakyDectector_stressData.sh $package $link $commitNum --stress $2 \"$testCommand\" $update $i"
    docker stop flakyDetector
    docker rm flakyDetector
    echo "Container Removed"
  done < $1
done
date '+%d.%b.%Y %T'