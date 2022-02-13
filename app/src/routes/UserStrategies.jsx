import React, {useState, useEffect} from "react";
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import { Grid } from '@mui/material';
import protectedFetch from '../auth/protectedFetch.js';
import StrategyCard from "../components/strategyCard.jsx";

function StrategyWriter() {
    const [loading, setLoading] = useState(true);
    const [strategies, setStrategies] = useState([]);

    useEffect(() => {
        protectedFetch("/api/get_strategies").then((data) => {
            setStrategies(data);
            setLoading(false);
            console.log(data);
        })
    }, [])
  
    return ( 
    <CenteredPageContainer>
        {loading ? null : strategies.map((object, i) => {
            return <StrategyCard name={object.name} winrate={object.avgWinRate} return={object.avgReturn} />
        })}
    </CenteredPageContainer>
    );
}
 
export default StrategyWriter;