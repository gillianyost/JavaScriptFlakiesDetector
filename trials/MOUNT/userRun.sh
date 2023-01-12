package=$1
link=$2
commitNum=$3
udpate=$4
# output="file.txt"
cd /home/flakie
git clone $link ./package # Run as user
cd package
git checkout $commitNum
# filename="package.json"
# while IFS= read -r packageline
# do
# if [[ "$packageline" == *"\"jest\":"* ]]
# then
#     testType=$(echo "$packageline" | cut -d'"' -f 4)
# fi
# done < "$filename"
# echo "JEST VERSION"
# echo "$testType"
# printf "$package, $testType\n" >> /home/flakie/fileout.txt
npm install
# currentver="$(jest --version)"
# requiredver="24.7.1"
#  if [ "$(printf '%s\n' "$requiredver" "$currentver" | sort -V | head -n1)" = "$requiredver" ]; then 
#         printf "${package} Greater than or equal to ${requiredver}\n" >> /home/flakie/fileout.txt
#  else
#         printf "${package} Less than ${requiredver}\n" >> /home/flakie/fileout.txt
#  fi 
# if [[ $update==0 ]]
# then
#     npm install jest@24.7.1
# fi
# npm install jest@24.7.1
npm run build