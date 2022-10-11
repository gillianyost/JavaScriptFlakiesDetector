sequencer=' --json --outputFile=testReport.txt'
flakySeq=' --json --outputFile=flakytestReport.txt'
package=$1
link=$2
commitNum=$3
option=$4
count=$5
testType=$6

cp ./home/projects/flakyDetector.py ./home/flakie


# USER
su - flakie
flaky setup.sh $link $commitNum
git clone $link ./package # Run as user
cd package
git checkout $commitNum
npm install
npm run build
echo "Built"
# testType="jest"
cd ..
testCommand="$testType$sequencer"
flaktTestCommand="$testType$flakySeq"
# python ./flakyDetector.py $package $count "$testCommand" "$flaktTestCommand"
# echo "Sucessful Run of Non-Stress Flaky Detector"
# stress-ng --cpu 6 --matrix 7 --mq 5 &
# pid_stress=$!
# python ./flakyDetector.py $package $count "$testCommand" "$flaktTestCommand"
# kill -9 "$pid_stress"
# echo "Sucessful Run of Stress Flaky Detector"

# ROOT
exit
if [ "$option" == "--stress" ]
then
  stress-ng --cpu 12 --matrix 9 --mq 5 &
  pid_stress=$!
fi

# USER
echo "Run Test"
su - flakie
flakie python ./flakyDetector.py $package $count "$testCommand" "$flaktTestCommand"

# ROOT
exit
# move files into mount area
if [ "$option" == "--stress" ]
then
  kill -9 "$pid_stress"
fi
cp ./home/flakie/data.cvs ./home/projects

# Move results into the mounted area

# rm -rf package # Not needed