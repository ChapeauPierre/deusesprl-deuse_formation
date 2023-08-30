import React from 'react'
import { render } from 'react-dom'

import HelloWorld from './HelloWorld';

var container = document.getElementById('react-helloworld');
render(
  <HelloWorld {...container.dataset}/>,
  container
)
