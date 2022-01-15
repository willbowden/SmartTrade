import React, { useState } from 'react';
import protectedFetch from "../auth/protectedFetch.js";
import LoadingOverlay from "../components/loadingOverlay.jsx";
import CandlestickChart from '../components/candlestickChart.jsx';
import '../App.css';

function ChartTest() {



    return(
        <div className="centered-div">
            {loading ? <LoadingOverlay /> : null }  
            <form><label>Symbol:</label> {/* Form for entering info */}
            <input type="text" value={symbol} onChange={e => {setSymbol(e.target.value)}}></input></form>
            <form><label>Timeframe:</label> {/* Form for entering info */}
            <input type="text" value={timeframe} onChange={e => {setTimeframe(e.target.value)}}></input></form>
            <form><label>Start Date:</label> {/* Form for entering info */}
            <input type="text" value={startDate} onChange={e => {setStartDate(e.target.value)}}></input></form>
            <CandlestickChart />
            <input className="button" type="button" value="Test" onClick={sendRequest} disabled={loading?true:null}></input>
        </div>
    );
}

export default ChartTest;