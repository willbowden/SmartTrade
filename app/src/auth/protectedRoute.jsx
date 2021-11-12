import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const PrivateRoute = () => {
  let logged = (localStorage.getItem('REACT_TOKEN_AUTH_KEY') != null) ? true : false;
  
  return logged ? (<Outlet />) : (<Navigate to="/login" />)
}

export default PrivateRoute;