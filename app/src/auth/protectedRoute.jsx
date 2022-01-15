import React, { useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import protectedFetch from './protectedFetch';

const PrivateRoute = React.memo(() => {
  const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem("isAuthenticated"));

  function refreshStatus() { // Verify the user's token
    protectedFetch('/api/verify_token').then(r => r.json()).then(result => {
      if (result.response !== 'ok') { // If their token isn't valid
        setIsAuthenticated(false); // Set the localStorage variable
        return (<Navigate to="/login" />); // Return them to login
      }
    })
  }
  
  setTimeout(refreshStatus, 300000) // Schedule the function to run 5 minutes from now 
  
  return (isAuthenticated ? <Outlet /> : <Navigate to="/login" />) // Return the appropriate component
});

export default PrivateRoute;