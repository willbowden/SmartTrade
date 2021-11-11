import React from 'react';
import { Navigate, Route } from 'react-router-dom'
import { useAuth } from './index';

const ProtectedRoute = ({ component: Component, ...rest }) => {
  const [logged] = useAuth();

  return <Route {...rest} render={(props) => (
    logged
      ? <Component {...props} />
      : <Navigate to='/login' />
  )} />
}

export default ProtectedRoute;