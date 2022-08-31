#!/bin/bash
sequencer=' --json --outputFile=testReport.txt'
while IFS= read -r package
do
  read -r link
  start=$(date +%s)
  git clone $link
  # npm pack $package
  # tar zxvf *.tgz
  
  cd $package
  commitNum=$(git log --pretty=format:'%h' -n 1)
  echo $commitNum

  filename="package.json"
  jest=0
  jas=0
  mocha=0
  karma=0
  while IFS= read -r packageline
  do
    if [[ "$packageline" == *"jest"* ]]
    then
        jest=1
    fi
    if [[ "$packageline" == *"jasmine"* ]]
    then
        jas=1
    fi
    if [[ "$packageline" == *"mocha"* ]]
    then
        mocha=1
    fi
    if [[ "$packageline" == *"karma"* ]]
    then
        karma=1
    fi
    if [[ "$packageline" == *"test\":"* ]]
    then
          testType=$(echo "$packageline" | cut -d'"' -f 4)
    fi
  done < "$filename"
  cd ..
  end=$(date +%s)
  echo "$package,$start,$end,$commitNum,$jest,$jas,$mocha,$karma,$testType" >> data.csv
  rm -rf "$package"
  # cd ..
  # testCommand="$testType$sequencer"
#   flaktTestCommand="$testType$flakySeq"
#   # echo $testCommand
  # python ./runtest.py $package $commitNum
  # jest --json --outputFile=testReport.txt
  # numFailedTestSuites=`jq '.numFailedTestSuites' testReport.txt`
  # numFailedTests=`jq '.numFailedTests' testReport.txt`
  # numPassedTestSuites=`jq '.numPassedTestSuites' testReport.txt`
  # numPassedTests=`jq '.numPassedTests' testReport.txt`
  # numPendingTestSuites=`jq '.numPendingTestSuites' testReport.txt`
  # numPendingTests=`jq '.numPendingTests' testReport.txt`
  # numRuntimeErrorTestSuites=`jq '.numRuntimeErrorTestSuites' testReport.txt`
  # numTotalTestSuites=`jq '.numTotalTestSuites' testReport.txt`
  # numTotalTests=`jq '.numTotalTests' testReport.txt`
  # rm testReport.txt

  #write data to file
  # cd ..
  # end=$(date +%s)
  # # echo "$package,$start,$end,$commitNum,$numFailedTestSuites,$numFailedTests,$numPassedTestSuites,$numPassedTests,$numPendingTestSuites,$numPendingTests,$numRuntimeErrorTestSuites,$numTotalTestSuites,$numTotalTests" >> data.csv
  # rm -rf "$package"
done < $1
