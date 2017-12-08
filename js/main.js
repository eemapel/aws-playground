import React from "react";
import ReactDOM from "react-dom";
import ExampleWork from "./example-work";

const myWork = [
  {
    'title': 'Suremoku',
    'href': 'http://bazaar.launchpad.net/~eemapel/suremoku/trunk/files',
    'desc': 'Qt/C++ Gomoku application',
    'image': {
      'desc': 'Screenshot of Gomoku app',
      'src': 'images/suremoku.png',
      'comment': ''
    }
  },
  {
    'title': 'Spotti',
    'href': 'http://bazaar.launchpad.net/~eemapel/spotti/trunk/files',
    'desc': "Simple Product Owner's Tool - Dependency Mapper",
    'image': {
      'desc': 'Screenshot of Spotti app',
      'src': 'images/spotti.png',
      'comment': ''
    }
  },
  {
    'title': 'Protein Finder',
    'href': 'http://ec2-54-88-196-50.compute-1.amazonaws.com',
    'desc': 'Web application to find matching proteins for given DNA sequence',
    'image': {
      'desc': 'Screenshot of Protein Finder',
      'src': 'images/proteinfinder.png',
      'comment': ''
    }
  }
]

ReactDOM.render(<ExampleWork work={myWork} />, document.getElementById('example-work'));
