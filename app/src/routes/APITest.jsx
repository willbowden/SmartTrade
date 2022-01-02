import React, { useState, useCallback } from 'react';
import protectedFetch from "../auth/protectedFetch.js";
import LoadingOverlay from "../components/loadingOverlay.jsx";
import '../App.css';

function APITest() {

    const[loading, setLoading] = useState(false);
    const[result, setResult] = useState('');
    const[endPoint, setEndPoint] = useState('/api/get_user_holdings');

    const sendRequest = (e) => {
        e.preventDefault();
        console.log(endPoint);
        setLoading(true);
        protectedFetch(endPoint).then(data => {
            setResult(JSON.stringify(data));
            setLoading(false);
        })
    };

    return(
        <div className="centered-div">
            {loading ? <LoadingOverlay /> : null }  
            <form><label>The API Endpoint Being Tested Is:</label>
            <input type="text" value={endPoint} onChange={e => {setEndPoint(e.target.value)}}></input></form>
            <p>Result: {result}</p>
            <input className="button" type="button" value="Test" onClick={sendRequest} disabled={loading?true:null}></input>
        </div>
    );
}

export default APITest;