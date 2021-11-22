import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const PrivateRoute = () => {
  const keyJSON = JSON.parse(localStorage.getItem('REACT_TOKEN_AUTH_KEY'));
  console.log(keyJSON)
  let token = null;
  if (keyJSON) {
    token = keyJSON.access_token;
  }

  const logged = token ? true : false;
  
  return logged ? (<Outlet />) : (<Navigate to="/login" />)
}

export default PrivateRoute;