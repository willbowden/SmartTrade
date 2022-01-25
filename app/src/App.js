import React from 'react';
import {Link, Outlet} from 'react-router-dom'
import LogoutButton from './components/logoutButton'
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';

function App() {

  const isAuthenticated = localStorage.getItem('isAuthenticated');

  return (
    <Box>
      <AppBar position="sticky" color="default">
        <Toolbar>
          <Button component={Link} to="/dashboard" variant="text">Dashboard</Button>
          <Button component={Link} to="/backtest" variant="text">Backtesting</Button>
          <Button component={Link} to="/api_test" variant="text">API Tester</Button>
          <Button component={Link} to="/chart_test" variant="text">chart_test</Button>
          <Box sx={{ flexGrow: 1 }} />
          {isAuthenticated ? null : <Button component={Link} to="/login" variant="text">Login</Button>}
          {isAuthenticated ? null : <Button component={Link} to="/register" variant="text">Register</Button>}
          <LogoutButton />
        </Toolbar>
      </AppBar>
      <Outlet />
    </Box>
  );
}

export default App;