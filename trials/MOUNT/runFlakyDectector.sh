append='_data.csv'
addon='_test.json'
package=$1
link=$2
commitNum=$3
option=$4
count=$5
testType=$7
update=$6

echo Test Type "$testType"
echo UPDATE $update

cp -v /home/projects/flakyDetector.py /home/flakie
cp -v /home/projects/RandomSequencerCompiled.js /home/flakie
cp -v /home/projects/test.json /home/flakie
cp -v /home/projects/fileout.txt /home/flakie/
chmod 777 /home/flakie/fileout.txt
chmod 777 /home/flakie/test.json

# USER
su -c "./home/projects/userRun.sh "$package" "$link" "$commitNum" $update" flakie
# ROOT
# comment back in
if [ "$option" == "--stress" ]
then
  stress-ng --class network, cpu, io, filesystem --all 1 &
  pid_stress=$!
fi

# USER
echo "Running"
cd /home/flakie
echo "$testType" >> command.txt
su -c "python ./flakyDetector.py "$package" "$count" "$update"" flakie

rm command.txt
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
mkdir -p /home/projects/"$currdate"/"$sub"/testReports
cp /home/flakie/"$output" /home/projects/"$currdate"/"$sub"
cp /home/flakie/"$flaky_out" /home/projects/"$currdate"/"$sub"

# Move results into the mounted area
echo "Moving Test Results"
cp -v /home/flakie/"testReport"* /home/projects/"$currdate"/"$sub"/testReports
cp -v /home/flakie/test.json /home/flakie/"$sub$addon"

cp -v /home/flakie/"$sub$addon" /home/projects/"$currdate"/"$sub"

chmod -R 777 /home/projects/"$currdate"

# chmod 777 /home/projects/"$currdate"/"$sub"/"$sub$addon"

# Jest Version Output
# cp /home/flakie/fileout.txt /home/projects
