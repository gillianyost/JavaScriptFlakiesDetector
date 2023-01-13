package=$1
link=$2
commitNum=$3
udpate=$4
cd /home/flakie
git clone $link ./package # Run as user
cd package
git checkout $commitNum
npm install
npm run build