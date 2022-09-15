sequencer=' --json --outputFile=testReport.txt'
flakySeq=' --json --outputFile=flakytestReport.txt'
package=$1
link=$2
commitNum=$3
option=$4
count=$5
testType=$6
git clone $link ./package # Run as user
cd package
git checkout $commitNum
npm install
npm run build
# testType="jest"
cd ..
testCommand="$testType$sequencer"
flaktTestCommand="$testType$flakySeq"
if [ "$option" == "--stress" ]
then
  stress-ng --cpu 12 --matrix 9 --mq 5 &
  pid_stress=$!
fi
python ./flakyDetector.py $package $count "$testCommand" "$flaktTestCommand"
# move files into mount area
if [ "$option" == "--stress" ]
then
  kill -9 "$pid_stress"
fi
rm -rf package # Not needed