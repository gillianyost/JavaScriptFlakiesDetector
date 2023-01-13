append='_data.csv'
package=$1
link=$2
commitNum=$3
option=$4
count=$5
testType=$6
update=$7

cp -v /home/projects/flakyDetector.py /home/flakie
cp -v /home/projects/RandomSequencerCompiled.js /home/flakie
cp -v /home/projects/test.json /home/flakie
cp -v /home/projects/fileout.txt /home/flakie/
chmod 777 /home/flakie/fileout.txt

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
cp /home/flakie/"testReport"* /home/projects/"$currdate"/"$sub"/testReports

# Jest Version Output
# cp /home/flakie/fileout.txt /home/projects
