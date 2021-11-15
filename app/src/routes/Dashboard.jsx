import React from "react";
import Clock from '../components/clock'
import '../App.css';
 
function Dashboard() {
  return ( 
    <div className="centered-div">
        <h1>Dashboard</h1>
        <Clock></Clock>
    </div>
  );
}
 
export default Dashboard;