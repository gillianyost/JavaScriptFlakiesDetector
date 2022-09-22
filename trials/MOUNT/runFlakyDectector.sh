sequencer=' --json --outputFile=testReport.txt'
flakySeq=' --json --outputFile=flakytestReport.txt'
append='_data.csv'
package=$1
link=$2
commitNum=$3
option=$4
count=$5
testType=$6

cp -v ./home/projects/flakyDetector.py ./home/flakie
# cd home/flakie
# echo "Working"
# mkdir -v package
# echo "Directory Made"
# cd ..
# cd ..
# cp ./home/projects/flakyDetector.py ./home/flakie
echo "COPY MOVED UPDATED"

# USER
# sudo -u flakie ./home/projects/userRun.sh "$package" "$link" "$commitNum"
su - flakie
alias jest='jest --json --outputFile=testReport.txt'
echo "$whoami"
git clone $link ./package # Run as user
cd package
git checkout $commitNum
npm install
npm run build
cd ..
testCommand="$testType$sequencer"
flaktTestCommand="$testType$flakySeq"
python ./flakyDetector.py $package $count "$testCommand" "$flaktTestCommand"
# echo "Sucessful Run of Non-Stress Flaky Detector"
# stress-ng --cpu 6 --matrix 7 --mq 5 &
# pid_stress=$!
# python ./flakyDetector.py $package $count "$testCommand" "$flaktTestCommand"
# kill -9 "$pid_stress"
# echo "Sucessful Run of Stress Flaky Detector"
# testCommand="$testType$sequencer"
# flaktTestCommand="$testType$flakySeq"
# ROOT
if [ "$option" == "--stress" ]
then
  stress-ng --cpu 12 --matrix 9 --mq 5 &
  pid_stress=$!
fi

# USER

su -c 'python ../home/projects/flakyDetector.py $package $count "$testCommand" "$flaktTestCommand"' flakie

# ROOT
# move files into mount area
if [ "$option" == "--stress" ]
then
  kill -9 "$pid_stress"
fi
sub=`echo "$package" | tr / _`
output="$sub$append"

# cp ./home/flakie/"$output" ./home/projects
# Flaky Tests Text file

# Move results into the mounted area

# rm -rf package # Not needed