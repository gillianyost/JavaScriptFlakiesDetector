date '+%d.%b.%Y %T'
while IFS="," read -r package link commitNum date testCommand
do
  echo "$package"
  # sub=`echo "$package" | tr / _`
  # append="_logOutput.txt"
  # log_file = "$sub$append"
  docker run -dit --name flakyDetector -v $(pwd):/home/projects node:lts-fermium-flakie
  docker exec flakyDetector /bin/bash -c "/home/projects/runFlakyDectector.sh $package $link $commitNum --no_stress $2 \"$testCommand\""
  docker stop flakyDetector
  docker rm flakyDetector
  # currdate=$(date +'%Y_%m_%d')
  # mv "$log_file" ./"$currdate"/"$sub"
  echo "Container Removed"
done < $1
date '+%d.%b.%Y %T'