import TestSequencer from '@jest/test-sequencer';

class CustomSequencer extends TestSequencer {
  sort(tests) {
    return tests.sort(() => {
      if(Math.random() > 0.5){
        return 1;
      }else{
        return -1;
      }
    });
  }
}

export default CustomSequencer;