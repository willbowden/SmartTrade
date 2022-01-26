import React, { useState } from 'react';
import protectedFetch from "../auth/protectedFetch.js";
import CandlestickChart from '../components/candlestickChart.jsx';
import '../App.css';

function ChartTest() {

    const[test, setTest] = useState('hello!');

    return(
        <div className="centered-div">
            <form><label>Test Text:</label> {/* Form for entering info */}
            <input type="text" value={test} onChange={e => {setTest(e.target.value)}}></input></form>
            <CandlestickChart test={test}></CandlestickChart>
        </div>
    );
}

export default ChartTest;