sequencer=' --json --outputFile=testReport.txt'
flakySeq=' --json --outputFile=flakytestReport.txt'
package=$1
link=$2
start=$(date +%s)
git clone $link ./package # Run as user
cd package
commitNum=$(git log --pretty=format:'%h' -n 1) # Run all git commands as user
echo $commitNum
npm install
npm run build
# filename="package.json"
# while IFS= read -r packageline
# do
#   if [ "$packageline" == *"test\":"* ]
#   then
#     testType=$(echo "$packageline" | cut -d'"' -f 4)
#   fi
# done < "$filename"
testType="jest"
cd ..
testCommand="$testType$sequencer"
flaktTestCommand="$testType$flakySeq"
if [ $3="--stress" ]
then
  stress-ng --matrix 0 &
  pid_stress=$!
fi
python ./flakyDetector.py $package 1 "$testCommand" "$flaktTestCommand"
# move files into mount area
if [ $3="--stress" ]
then
  kill -9 "$pid_stress"
fi
rm -rf package # Not needed