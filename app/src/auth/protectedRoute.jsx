import React, { useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import protectedFetch from './protectedFetch';
import LoadingOverlay from '../components/loadingOverlay';

const PrivateRoute = React.memo(() => {
  const[loggedIn, setLoggedIn] = useState(false)
  const[loading, setLoading] = useState(true);

  protectedFetch("/verify_token").then(data => {
    if (data.response == 'ok') {
      setLoggedIn(true);
      setLoading(false);
    } else {
      setLoggedIn(false);
      setLoading(false);
    };
  })
  
  return loading ? <LoadingOverlay /> : (loggedIn ? <Outlet /> : <Navigate to="/login" />)
});

export default PrivateRoute;