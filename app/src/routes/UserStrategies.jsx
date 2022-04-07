import React, {useState, useEffect} from "react";
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import {Navigate} from 'react-router-dom';
import { Grid } from '@mui/material';
import protectedFetch from '../auth/protectedFetch.js';
import StrategyCard from "../components/strategyCard.jsx";
import BacktestList from "../components/backtestList.jsx";
import BacktestResults from "./BacktestResults.jsx";
import { fromUnixTime } from "date-fns";

function UserStrategies(props) {
    const [loading, setLoading] = useState(true);
    const [strategies, setStrategies] = useState([]);
    const [showBacktests, setShowBacktests] = useState(false);
    const [backtestResults, setBacktestResults] = useState([]);
    const [showBacktestResults, setShowResults] = useState(false);
    const [strategyBacktests, setStrategyBacktests] = useState([]);
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

    const stopViewingBacktests = () => {
        setShowBacktests(false);
        setShowResults(false);
    }

    const viewBacktests = (strategyName) => {
        let payload = {
            strategyName: strategyName
        }

        protectedFetch("/api/get_strategy_backtests", {
            method: 'POST',
            body: JSON.stringify(payload)
        }).then((result) => {
            setStrategyBacktests(result);
            console.log(result);
            setShowBacktests(true);
        })
    }

    const viewBacktestResults = (backtestID) => {
        let payload = {
            backtestID: backtestID
        }

        protectedFetch("/api/get_backtest_results", {
            method: 'POST',
            body: JSON.stringify(payload)
        }).then((result) => {
            console.log(result);
            let id = 0;
            let newOrderHistory = []
            result.orderHistory.forEach((row) => {
                let newRow = row;
                newRow.id = id;
                newRow.timestamp = fromUnixTime(newRow.timestamp / 1000);
                newOrderHistory.push(newRow)
                id += 1;
            })
            result.orderHistory = newOrderHistory;
            setBacktestResults(result);
            setShowResults(true);
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
        {loading || showBacktests ? null : strategies.map((object, i) => {
            return <StrategyCard name={object.name}
             winrate={object.avgWinRate} return={object.avgReturn}
             selectStrategy={props.selectStrategy}
              deleteStrategy={deleteStrategy} 
              viewBacktests={viewBacktests}/>
        })}
        { showBacktests ? <BacktestList backtests={strategyBacktests} getResults={viewBacktestResults} hide={stopViewingBacktests}/> : null }
        { showBacktestResults ? <BacktestResults results={backtestResults}></BacktestResults> : null }
    </CenteredPageContainer>
    );
}
 
export default UserStrategies;