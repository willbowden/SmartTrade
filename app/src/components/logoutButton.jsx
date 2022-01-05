import React from 'react';
import { logout } from "../auth"
import { useNavigate } from "react-router-dom";
import '../App.css';

function LogoutButton() {
    const navigate = useNavigate();

    const onLogoutClick = (e) => {
        e.preventDefault();
        logout();
        localStorage.setItem('isAuthenticated', "false")
        navigate("/login")
    }

    return (
        <button onClick={onLogoutClick}>Logout</button>
    )
}

export default LogoutButton;