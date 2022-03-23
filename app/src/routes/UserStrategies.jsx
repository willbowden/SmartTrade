import React, {useState, useEffect} from "react";
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import {Navigate} from 'react-router-dom';
import { Grid } from '@mui/material';
import protectedFetch from '../auth/protectedFetch.js';
import StrategyCard from "../components/strategyCard.jsx";

function UserStrategies(props) {
    const [loading, setLoading] = useState(true);
    const [strategies, setStrategies] = useState([]);
    const [redirectToLogin, setRedirect] = useState(false);
    const [shouldRefresh, setShouldRefresh] = useState(false);

    const deleteStrategy = (strategyName) => {
        let payload = {
            strategyName: strategyName
        }
        protectedFetch("/api/delete_strategy", {
            method: 'POST',
            body: JSON.stringify(payload)
        }).then(() => {
            setShouldRefresh(!shouldRefresh);
        }).catch(() => {
            setRedirect(true);
        })
    }

    useEffect(() => {
        protectedFetch("/api/get_strategies").then((data) => {
            setStrategies(data);
            setLoading(false);
            console.log(data);
        }).catch(() => {
            setRedirect(true); // Redirect to login page if user is unauthorised.
        })
    }, [shouldRefresh])
  
    return ( 
    <CenteredPageContainer>
        {redirectToLogin && <Navigate to="/login"></Navigate>}
        {loading ? null : strategies.map((object, i) => {
            return <StrategyCard name={object.name}
             winrate={object.avgWinRate} return={object.avgReturn}
             selectStrategy={props.selectStrategy}
              deleteStrategy={deleteStrategy} />
        })}
    </CenteredPageContainer>
    );
}
 
export default UserStrategies;