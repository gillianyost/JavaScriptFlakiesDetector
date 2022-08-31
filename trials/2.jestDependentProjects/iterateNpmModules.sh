#!/bin/bash
while IFS= read -r package
do
  echo "$package"
  npm pack $package
  tar zxvf *.tgz
  cd package
  npm install
  npm run build
  cd ..
  sh ./flakyDetector.sh $package 10
  rm -rf *.tgz package
done < $1