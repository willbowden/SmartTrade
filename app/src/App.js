import React from 'react';
import './App.css';
import {
  Route,
  Routes,
  NavLink,
  HashRouter
} from "react-router-dom";
import Home from "./Home.js";

function App() {
  return (
    <HashRouter>
      <div>
        <div class="navbar">
          <ul>
            <li><NavLink to="/">Home</NavLink></li>
            <li><NavLink to="/strategies">Strategy Editor</NavLink></li>
            <li><NavLink to="/backtest">Backtesting</NavLink></li>
          </ul>
        </div>
        <body>
          <div class="page">
            <Routes>
              <Route path="/" component={Home}/>
            </Routes>
          </div>
        </body>
      </div>
    </HashRouter>
  );
}

export default App;
