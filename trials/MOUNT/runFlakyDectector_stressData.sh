append='_data.csv'
package=$1
link=$2
commitNum=$3
option=$4
count=$5
testType=$6
update=$7
stress=$8

cp -v /home/projects/flakyDetector.py /home/flakie
cp -v /home/projects/RandomSequencerCompiled.js /home/flakie
cp -v /home/projects/test.json /home/flakie
cp -v /home/projects/fileout.txt /home/flakie/
chmod 777 /home/flakie/fileout.txt

# USER
su -c "./home/projects/userRun.sh "$package" "$link" "$commitNum" $update" flakie
# ROOT
ng_class=""
echo NEW STRESS
echo $update
echo $stress
if [ "$option" == "--stress" ]
then
  echo "IN STRESS"
  case $stress in
  1)
    echo "NETWORK"
    ng_class="network"
    stress-ng --class network --all 1 &
    pid_stress=$!
    ;;
  2)
    echo "CPU"
    ng_class="cpu"
    stress-ng --class cpu --all 1 &
    pid_stress=$!
    ;;
  3)
    echo "IO"
    ng_class="io"
    stress-ng --class io --all 1 &
    pid_stress=$!
    ;;
  4) 
    echo "FILESYSTEM"
    ng_class="filesystem"
    stress-ng --class filesystem --all 1 &
    pid_stress=$!
    ;;
  5)
    echo "SCEDULE"
    ng_class="schedule"
    stress-ng --class scheduler --all 1 &
    pid_stress=$!
    ;;
  6)
    echo "NO STRESS"
    ng_class="no_stress"
    ;;
  esac
fi

# USER
echo "Running"
cd /home/flakie
echo "$testType" >> command.txt
start=$(date +%s)
su -c "python ./flakyDetector.py "$package" "$count" "$update"" flakie
end=$(date +%s)
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
cp /home/flakie/package/"testReport"* /home/projects/"$currdate"/"$sub"/testReports
printf "$sub,$ng_class,$start,$end\n" >> /home/projects/stressData.csv

# Jest Version Output
# cp /home/flakie/fileout.txt /home/projects
