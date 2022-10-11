#!/bin/bash
sequencer=' --testSequencer=../RandomSequencerCompiled.js --json --outputFile=testReport.txt'
flakySeq=' --testSequencer=../RandomSequencerCompiled.js --json --outputFile=flakytestReport.txt'
package=$1
echo "$package"
npm pack $package
tar zxvf *.tgz
cd /home/project/package
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
cd /home/project
testCommand="$testType$sequencer"
flaktTestCommand="$testType$flakySeq"
python ./flakyDetector.py $package 5 "$testCommand" "$flaktTestCommand"
rm -rf *.tgz package