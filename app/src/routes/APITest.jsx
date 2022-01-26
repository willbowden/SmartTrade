import React, { useState } from 'react';
import protectedFetch from "../auth/protectedFetch.js";
import '../App.css';

function APITest() {

    const[loading, setLoading] = useState(false);
    const[result, setResult] = useState('');
    const[endPoint, setEndPoint] = useState('/api/get_user_holdings');

    const sendRequest = (e) => { // Send a request to the api endpoint of choice
        e.preventDefault();
        console.log(endPoint);
        setLoading(true);
        protectedFetch(endPoint).then(data => {
            setResult(JSON.stringify(data)); // Stringify response and display it to screen
            setLoading(false);
        })
    };

    return(
        <div className="centered-div">
            {loading ? null : null }  
            <form><label>The API Endpoint Being Tested Is:</label> {/* Form for entering API endpoint */}
            <input type="text" value={endPoint} onChange={e => {setEndPoint(e.target.value)}}></input></form>
            <p>Result: {result}</p>
            <input className="button" type="button" value="Test" onClick={sendRequest} disabled={loading?true:null}></input>
        </div>
    );
}

export default APITest;