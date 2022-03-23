import React, {useState} from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import protectedFetch from './protectedFetch';

const PrivateRoute = function () {
  const [isAuthenticated, setIsAuthenticated] = useState(JSON.parse(localStorage.getItem("isAuthenticated")));
  
  return (isAuthenticated ? <Outlet /> : <Navigate to="/login" />) // Return the appropriate component
};

export default PrivateRoute;