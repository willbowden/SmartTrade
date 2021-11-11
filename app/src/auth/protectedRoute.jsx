import React from 'react'
import { Navigate, Route } from 'react-router-dom'

function ProtectedRoute({ isAuthenticated, component: Component, ...rest }) {
  console.log("this", isAuthenticated);

  return (
    <Route
      {...rest}
      render={(props) =>
        isAuthenticated ? <Component {...props} /> : <Navigate to="/login" />
      }
    />
  );
}

export default ProtectedRoute;