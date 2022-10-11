#!/bin/bash
sequencer=' --json --outputFile=testReport.txt'
mocha='--reporter-option output=filename.json'
while IFS= read -r package
do
#     PACKAGE_NAME=""
#     LINK=""
#   export package
#   export PACKAGE_NAME
#   export LINK

# #   python -c 'import os'
#   python -c 'import os
# var = os.environ["package"]
# splitVar = (var.split())
# packageName = splitVar[0].split("/")
# os.environ['PACKAGE_NAME'] = packageName[1]
# os.environ['LINK'] = splitVar[-1]'
#     echo "$PACKAGE_NAME"
#     echo "$LINK"
    read -r link
#   python -c 'print(package.split())'
#   echo "$package"
  start=$(date +%s)
  git clone $link
  # npm pack $package
  # tar zxvf *.tgz
  
  cd $package
  commitNum=$(git log --pretty=format:'%h' -n 1)
  echo $commitNum
  npm install
  npm run build

  # while IFS= read -r packageline
  # do
  #   if [[ "$packageline" == *"test\":"* ]]
  #   then
  #     testType=$(echo "$packageline" | cut -d'"' -f 4)
  #   fi
  # done < "$filename"

  # cd ..
  # testCommand="$testType$sequencer"
#   flaktTestCommand="$testType$flakySeq"
#   # echo $testCommand
  # python ./runtest.py $package $commitNum
  jest --json --outputFile=testReport.txt
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
  end=$(date +%s)
  echo "$package,$start,$end,$commitNum,$numFailedTestSuites,$numFailedTests,$numPassedTestSuites,$numPassedTests,$numPendingTestSuites,$numPendingTests,$numRuntimeErrorTestSuites,$numTotalTestSuites,$numTotalTests" >> data.csv
  rm -rf "$package"
done < $1
