import Resource from './Resource';

export default class ResourceInitializer{
  constructor(){
    this.resource = new Resource();
  }
  initialize(){
    this.resource.initialize();
  }
}
