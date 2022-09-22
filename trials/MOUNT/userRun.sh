sequencer=' --json --outputFile=testReport.txt'
flakySeq=' --json --outputFile=flakytestReport.txt'
append='_data.csv'
package=$1
link=$2
commitNum=$3
cd ./home/flakie
alias jest='jest --json --outputFile=testReport.txt'
alias
git clone $link ./package # Run as user
cd package
git checkout $commitNum
npm install
npm run build
cd ..
cd ..
echo "jest"
# pwd