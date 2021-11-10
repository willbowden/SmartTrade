import React from 'react';
import './App.css';
import LogoutButton from './components/logoutButton.jsx';
import {Outlet, Link} from "react-router-dom";

function App() {
  return (
    <div class="fullsize">
      <div class="navbar">
        <ul>
          <li><Link to="/dashboard">Home</Link></li>
          <li><Link to="/backtest">Backtesting</Link></li>
          <li><Link to="/login">Login</Link></li>
          <LogoutButton />
        </ul>
      </div>
      <Outlet />
    </div>
  );
}

export default App;
