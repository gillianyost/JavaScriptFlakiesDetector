import * as fs from 'fs'

class Resource {
  initialize() {
    fs.writeFile('resourceFile.txt', 'Hello content!', () => {}); 

    let myGreeting = setTimeout(() => {
      fs.unlink('resourceFile.txt', () => {});
    }, 2000);
  }

  get() {
    return fs.existsSync('resourceFile.txt');
  }
}

export default Resource;
