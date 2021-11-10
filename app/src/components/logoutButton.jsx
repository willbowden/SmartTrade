import React from 'react';
import { logout } from "../auth"
import { useNavigate } from "react-router-dom";
import '../App.css';

function LogoutButton() {
    const navigate = useNavigate();

    const onLogoutClick = (e) => {
        e.preventDefault();
        logout();
        navigate("/dashboard");
    }

    return (
        <li><button onClick={onLogoutClick}>Logout</button></li>
    )
}

export default LogoutButton;