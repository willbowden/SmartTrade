import React, {useState} from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import protectedFetch from './protectedFetch';

const PrivateRoute = function () {
  const [isAuthenticated, setIsAuthenticated] = useState(JSON.parse(localStorage.getItem("isAuthenticated")));

  function refreshStatus() { // Verify the user's token
    try {
      protectedFetch('/api/verify_token').then(result => {
        return
      })
    } catch (err) {
      localStorage.setItem('isAuthenticated', 'false')
      setIsAuthenticated(false);
    }
  }
  
  setTimeout(refreshStatus, 300000) // Schedule the function to run 5 minutes from now 
  
  return (isAuthenticated ? <Outlet /> : <Navigate to="/login" />) // Return the appropriate component
};

export default PrivateRoute;