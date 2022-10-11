#!/bin/bash
while IFS= read -r package
do
  read -r link
  date=$(date)
  git clone $link
  cd $package
  fullName=$(git config --get remote.origin.url | sed 's/.*\/\([^ ]*\/[^.]*\).*/\1/')
  commitNum=$(git log --pretty=format:'%h' -n 1)
  echo $commitNum
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
  echo "$fullName,$link,$commitNum,$date" >> jestSubjectsFinal.csv
  rm -rf "$package"
done < $1
