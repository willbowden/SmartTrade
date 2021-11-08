import React, { useState, useCallback } from 'react';
import '../App.css';

function Clock() {

    const [currentTime, setCurrentTime] = useState(0);

    const sendRequest = useCallback(() => {
        fetch('/time').then(res => res.json()).then(data => {
        setCurrentTime(data.time);
    });
    }, []);

    return(
        <div class="div-centered">
            <p>The current time is {currentTime}</p>
            <input class="button" type="button" value="Test" onClick={sendRequest}></input>
        </div>
    );
}

export default Clock;