import ResourceInitializer from './ResourceInitializer';

let resourceInitializer = new ResourceInitializer();

test('initializes resource', () => {
  resourceInitializer.initialize();
});