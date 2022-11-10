package=$1
link=$2
commitNum=$3
cd /home/flakie
git clone $link ./package # Run as user
npm install jest @jest/test-sequencer
cd package
git checkout $commitNum
# npm install
# npm run build