import React, { useState, useCallback } from 'react';
import protectedFetch from "../auth/protectedFetch.js";

function Clock() {

    const [currentTime, setCurrentTime] = useState(0);

    const sendRequest = useCallback(() => {
        protectedFetch('/time').then(data => {
            setCurrentTime(data.time);
        })
    }, []);

    return(
        <div className="centered-div">
            <p>The current time is {currentTime}</p>
            <input class="button" type="button" value="Test" onClick={sendRequest}></input>
        </div>
    );
}

export default Clock;