const TestSequencer = require('@jest/test-sequencer').default;

class CustomSequencer extends TestSequencer {
  sort(tests) {
     let currentIndex = tests.length, randomIndex;
	
     while (currentIndex != 0) {
	randomIndex = Math.floor(Math.random() * currentIndex);
	currentIndex--;
		
	[tests[currentIndex], tests[randomIndex]] = [tests[randomIndex], tests[currentIndex]];
     }
     return tests;
  };
}

export default CustomSequencer;

// unbiased shuffle algorithm Fisher-Yates (Knuth) Shuffle
