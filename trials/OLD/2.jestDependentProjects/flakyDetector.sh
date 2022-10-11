#!/bin/bash

cd package
counter=0
flakyDetected=false
numPreviousFailedTests=-1

#detect flaky tests
while [ $counter -lt $2 ] && [ "$flakyDetected" = false ]
do
  npm run test -- --json --outputFile=testReport.txt
  numCurrentFailedTests=`jq '.numFailedTests' testReport.txt`
  echo "$numPreviousFailedTests, $numCurrentFailedTests"
  if [ $numPreviousFailedTests -ne -1 ] && [ $numCurrentFailedTests -ne $numPreviousFailedTests ]
  then
    flakyDetected=true
  else
    numPreviousFailedTests=$numCurrentFailedTests
  fi
  rm testReport.txt
  counter=$(( $counter + 1 ))
done

#collect other data
npm run test -- --json --outputFile=testReport.txt
numFailedTestSuites=`jq '.numFailedTestSuites' testReport.txt`
numFailedTests=`jq '.numFailedTests' testReport.txt`
numPassedTestSuites=`jq '.numPassedTestSuites' testReport.txt`
numPassedTests=`jq '.numPassedTests' testReport.txt`
numPendingTestSuites=`jq '.numPendingTestSuites' testReport.txt`
numPendingTests=`jq '.numPendingTests' testReport.txt`
numRuntimeErrorTestSuites=`jq '.numRuntimeErrorTestSuites' testReport.txt`
numTotalTestSuites=`jq '.numTotalTestSuites' testReport.txt`
numTotalTests=`jq '.numTotalTests' testReport.txt`
rm testReport.txt

#write data to file
cd ..
echo "$1,$flakyDetected,$numFailedTestSuites,$numFailedTests,$numPassedTestSuites,$numPassedTests,$numPendingTestSuites,$numPendingTests,$numRuntimeErrorTestSuites,$numTotalTestSuites,$numTotalTests" >> data.csv