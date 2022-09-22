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
# USER
su -c "./home/projects/userRun.sh "$package" "$link" "$commitNum"" flakie
# testCommand="$testType$sequencer"
# flaktTestCommand="$testType$flakySeq"
# ROOT
if [ "$option" == "--stress" ]
then
  stress-ng --cpu 12 --matrix 9 --mq 5 &
  pid_stress=$!
fi

# USER
cd ./home/flakie
echo $count
# testType="jest --json --outputFile=testReport.txt"
su -c "python ./flakyDetector.py "$package" "$count" "$testType"" flakie
cd ..
cd ..
# ROOT
# move files into mount area
if [ "$option" == "--stress" ]
then
  kill -9 "$pid_stress"
fi
sub=`echo "$package" | tr / _`
out="_flakies.txt"
output="$sub$append"
flaky_out="$sub$out"
currdate=$(date +'%Y_%m_%d')
mkdir -p ./home/projects/"$currdate"
cp ./home/flakie/"$output" ./home/projects/"$currdate"/
cp ./home/flakie/"$flaky_out" ./home/projects/"$currdate"/
# Flaky Tests Text file

# Move results into the mounted area

# rm -rf package # Not needed