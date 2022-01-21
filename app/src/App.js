import React from 'react';
import './App.css';
import './Navbar.css';
import {Link, Outlet} from 'react-router-dom'
import LogoutButton from './components/logoutButton'
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';

function App() {

  const isAuthenticated = localStorage.getItem('isAuthenticated');

  return (
    <div className='fullsize'>
      <AppBar position="static">
        <Toolbar>
          <Button component={Link} to="/dashboard" variant="contained">Dashboard</Button>
          <Button component={Link} to="/backtest" variant="text">Backtesting</Button>
          <Button component={Link} to="/api_test" variant="text">API Tester</Button>
          <Button component={Link} to="/chart_test" variant="text">chart_test</Button>
          {isAuthenticated && (<Button component={Link} to="/login" variant="text">Login</Button>)}
          {isAuthenticated && (<Button component={Link} to="/register" variant="text">Register</Button>)}
          <LogoutButton />
        </Toolbar>
      </AppBar>
      <Outlet />
    </div>
  );
}

export default App;