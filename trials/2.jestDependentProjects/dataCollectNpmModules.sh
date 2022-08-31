#!/bin/bash
input="multi-suite-npm-modules.txt"
while IFS= read -r line
do
  echo "$line"
  npm pack $line
  tar zxf *.tgz
  cd package
  filename="package.json"
  lang="JavaScript"
  while IFS= read -r packageline
  do
    if [[ "$packageline" == *".ts"* ]]
    then
        lang="Typescript"
    fi
    if [[ "$packageline" == *"test\":"* ]]
    then
          testType=$(echo "$packageline" | cut -d'"' -f 4)
    fi
  done < "$filename"
  cd ..
  rm -rf *.tgz package
  echo -n "$line," >> data.csv
  echo -n "$lang," >> data.csv
  echo "$testType" >> data.csv
done < "$input"