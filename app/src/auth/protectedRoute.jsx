import React, {useEffect, useState} from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import protectedFetch from './protectedFetch';

const PrivateRoute = function () {
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  useEffect(() => {
    protectedFetch("/api/verify_token").catch((err) => {
      setIsAuthenticated(false);
    })
  }, [])
  
  return (isAuthenticated ? <Outlet /> : <Navigate to="/login" />) // Return the appropriate component
};

export default PrivateRoute;