import React from 'react'
import { useAuth } from './index.js';
import { Navigate, Route } from 'react-router-dom'
import { Loading } from '../components/loading.jsx';

function RequireAuth({ children }) {
  let auth = useAuth();
  return (
    <Route>
      render={({ location }) =>
        auth.loading ? 
        <Loading /> :
        auth.user ? (
          children
        ) : (
          <Navigate to={{pathname: "/login", state: { from: location }}}/>
        )}
    </Route>
  )
}

export default RequireAuth;