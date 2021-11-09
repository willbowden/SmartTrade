import React from 'react';
import './App.css';
import {Outlet, Link} from "react-router-dom";

function App() {
  return (
    <div class="fullsize">
      <div class="navbar">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/backtest">Backtesting</Link></li>
        </ul>
      </div>
      <Outlet />
    </div>
  );
}

export default App;
