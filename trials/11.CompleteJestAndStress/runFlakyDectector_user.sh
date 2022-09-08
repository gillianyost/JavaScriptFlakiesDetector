sequencer=' --json --outputFile=testReport.txt'
flakySeq=' --json --outputFile=flakytestReport.txt'
package=$1
link=$2
commitNum=$3
option=$4
count=$5
testType=$6
su -c "git clone $link ./package" flakie # Run as user
cd package
su -c "git checkout $commitNum" flakie
npm install
npm run build
# testType="jest"
cd ..
testCommand="$testType$sequencer"
flaktTestCommand="$testType$flakySeq"
if [ "$option" == "--stress" ]
then
  stress-ng --cpu 2 --matrix 1 --mq 3 &
  pid_stress=$!
fi
su -c "python ./flakyDetector.py $package $count "$testCommand" "$flaktTestCommand"" flakie
# move files into mount area
if [ "$option" == "--stress" ]
then
  kill -9 "$pid_stress"
fi
rm -rf package # Not needed