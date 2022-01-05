import React, { useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import protectedFetch from './protectedFetch';
import LoadingOverlay from '../components/loadingOverlay';

const PrivateRoute = React.memo(() => {
  const isAuthenticated = localStorage.getItem("isAuthenticated");
  
  return (isAuthenticated ? <Outlet /> : <Navigate to="/login" />)
});

export default PrivateRoute;