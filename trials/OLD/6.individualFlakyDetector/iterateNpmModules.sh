#!/bin/bash
sequencer=' --testSequencer=../RandomSequencerCompiled.js --json --outputFile=testReport.txt'
flakySeq=' --testSequencer=../RandomSequencerCompiled.js --json --outputFile=flakytestReport.txt'
while IFS= read -r package
do
  echo "$package"
  npm pack $package
  tar zxvf *.tgz
  cd package
  npm install
  npm run build
  filename="package.json"
  while IFS= read -r packageline
  do
    if [[ "$packageline" == *"test\":"* ]]
    then
      testType=$(echo "$packageline" | cut -d'"' -f 4)
    fi
  done < "$filename"
  cd ..
  testCommand="$testType$sequencer"
  flaktTestCommand="$testType$flakySeq"
  echo $testCommand
  python ./flakyDetector.py $package 35 "$testCommand" "$flaktTestCommand"
  rm -rf *.tgz package
done < $1
