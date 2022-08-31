import Resource from './Resource';

export default class ResourceConsumer{
  constructor(){
    this.resource = new Resource();
  }
  consume(){
    return this.resource.get();
  }
}
