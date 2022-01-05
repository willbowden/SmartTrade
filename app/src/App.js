import React from 'react';
import './App.css';
import './Navbar.css';
import {Link, Outlet} from 'react-router-dom'
import LogoutButton from './components/logoutButton'

function App() {

  const isAuthenticated = localStorage.getItem('isAuthenticated');

  return (
    <div className="fullsize">
      <div className="navbar">
        <ul>
          <li><Link to="/dashboard">Home</Link></li>
          <li><Link to="/backtest">Backtesting</Link></li>
          <li><Link to="/api_test">API Tester</Link></li>
          {isAuthenticated ?  <li><Link to="/login">Login</Link></li> : null}
          {isAuthenticated ? <li><Link to="/register">Register</Link></li> : null}
          <LogoutButton />
        </ul>
      </div>
      <Outlet />
    </div>
  );
}

export default App;