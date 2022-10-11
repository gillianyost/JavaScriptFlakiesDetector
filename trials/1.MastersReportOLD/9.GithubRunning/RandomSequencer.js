import testData from "./test.json"
const TestSequencer = require('@jest/test-sequencer').default;
const seedrandom = require('seedrandom');
const fs = require('fs');

class CustomSequencer extends TestSequencer {
  sort(tests) {
    tests.sort((testA, testB) => (testA.path > testB.path ? 1 : -1));
    const lastTest = testData[testData.length - 1];
    let generator;
    if (lastTest.flakyTestDetected) {
      console.log("Seed: ", lastTest.seed.toString())
      generator = seedrandom(lastTest.seed.toString());
      const newTest = {seed:lastTest.seed};
      testData.push(newTest);
      const newData = JSON.stringify(testData);
      fs.writeFile('test.json', newData, (err) => {});
    } else {
      const newSeed = Math.random();
      console.log("Seed: ", newSeed)
      generator = seedrandom(newSeed.toString());
      const newTest = {seed:newSeed};
      testData.push(newTest);
      const newData = JSON.stringify(testData);
      fs.writeFile('test.json', newData, (err) => {});
    }
    for (var i = tests.length - 1; i > 0; i--) {
      const value = generator()
      console.log("Value: ", value)
      var j = Math.floor(value * (i + 1));
      var temp = tests[i];
      tests[i] = tests[j];
      tests[j] = temp;
    }
    // Durstenfeld Shuffle - updated due to the Fisher-Yates not working correctly for 2 test suites
    // Actually was not the issue, but Durstenfeld is more optimized version of Fisher-Yates so it will remain
     return tests;
  };
}

export default CustomSequencer;
