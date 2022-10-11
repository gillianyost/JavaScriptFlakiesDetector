#!/bin/bash
while IFS="," read -r package link commitNum date
do
  git clone $link ./package
  cd package
  git checkout $commitNum
  filename="package.json"
  while IFS= read -r packageline
  do
    if [[ "$packageline" == *"test\":"* ]]
    then
      testType=$(echo "$packageline" | cut -d'"' -f 4)
    fi
  done < "$filename"

  #write data to file
  cd ..
  echo "$testType" >> jestSubjectsCommand.csv
  rm -rf package
done < $1
