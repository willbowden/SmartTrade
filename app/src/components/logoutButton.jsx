import React from 'react';
import { logout } from "../auth"
import { useNavigate } from "react-router-dom";
import '../App.css';
import Button from '@mui/material/Button';


function LogoutButton() {

    const onLogoutClick = (e) => {
        e.preventDefault();
        logout();
        localStorage.setItem('isAuthenticated', 'false')
        navigate("/login")
    }

    return (
        <Button onClick={onLogoutClick}>Logout</Button>
    )
}

export default LogoutButton;