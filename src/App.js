import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
// import logo from './logo.svg';
import './App.css';
import TestComponent from './TestComponent'

class App extends Component {
  render() {
    return (
        <MuiThemeProvider>
            <TestComponent />
        </MuiThemeProvider>
    );
  }
}

export default App;
