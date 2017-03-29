import React, { Component } from 'react';
import {yellow500} from 'material-ui/styles/colors';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import './App.css';
import TestComponent from './TestComponent'


const muiTheme = getMuiTheme({
    palette: {
        primary1Color: yellow500,
    },
    appBar: {
        height: 50,
    },
});

class App extends Component {
  render() {
    return (
        <MuiThemeProvider muiTheme={muiTheme}>
            <TestComponent />
        </MuiThemeProvider>
    );
  }
}

export default App;
