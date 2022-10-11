import ResourceConsumer from './ResourceConsumer';

let resourceConsumer = new ResourceConsumer();

test('consumes resource', () => {
  expect(resourceConsumer.consume()).toBe(true);
});