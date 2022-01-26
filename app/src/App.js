import React from 'react';
import {useState} from 'react';
import {Link, Outlet} from 'react-router-dom'
import { AppBar, Button, Box, Toolbar } from '@mui/material';
import { logout } from "./auth"
import { useNavigate } from "react-router-dom";

function App() {
  const navigate = useNavigate();

  const [isAuthenticated, setIsAuthenticated] = useState(JSON.parse(localStorage.getItem('isAuthenticated')));

  const onLogoutClick = (e) => {
    e.preventDefault();
    logout();
    localStorage.setItem('isAuthenticated', 'false');
    setIsAuthenticated('false');
    navigate("/login");
  }

  return (
    <>
      <AppBar position="sticky" color="default" style={{ height: '8vh', display: 'flex', justifyContent: 'center'}}>
        <Toolbar>
          <Button component={Link} to="/dashboard" variant="text">Dashboard</Button>
          <Button component={Link} to="/backtest" variant="text">Backtesting</Button>
          <Button component={Link} to="/api_test" variant="text">API Tester</Button>
          <Button component={Link} to="/chart_test" variant="text">chart_test</Button>
          <Box sx={{ flexGrow: 1 }} />
          {isAuthenticated?  null : <Button component={Link} to="/login" variant="text">Login</Button>}
          {isAuthenticated ?  null : <Button component={Link} to="/register" variant="text">Register</Button>}
          {isAuthenticated ? <Button onClick={onLogoutClick}>Logout</Button> : null}
        </Toolbar>
      </AppBar>
        <Outlet />
    </>
  );
}

export default App;