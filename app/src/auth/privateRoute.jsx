import React from 'react'
import { useAuth } from './index.js';
import { Navigate, useLocation } from 'react-router-dom'

function RequireAuth({ children }) {
    let [loggedIn] = useAuth();
    console.log("User is logged in?" + loggedIn);
    let location = useLocation();
    console.log(location);
  
    if (!loggedIn) {
      return <Navigate to="/login" state={{ from: location }} />;
    }
  
    return children;
  }

export default RequireAuth;