import React, {useState, useEffect} from "react";
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import { Grid, Button } from '@mui/material';
import IndicatorSelector from "../components/indicatorSelector.jsx";
import RuleMaker from "../components/ruleMaker.jsx";
import StrategyDetails from '../components/strategyDetails.jsx';
import protectedFetch from '../auth/protectedFetch.js';
import { Navigate } from 'react-router-dom';

function StrategyWriter(props) {
  const [stage, setStage] = useState(0);
  const [indicators, setIndicators] = useState([]);
  const [rules, setRules] = useState({});
  const [asDict, setAsDict] = useState({});
  const [redirectToStrategies, setRedirect] = useState(false);
  if (props.state) {
    setIndicators(props.state.indicators);
    setRules(props.state.rules);
    setAsDict(props.state.asDict);
  }

  const chooseIndicators = (chosen) => {
    setIndicators(chosen);
    console.log(chosen);
    setStage(1);
  }

  const addRules = (buyRules, sellRules) => {
    let temp = rules;
    temp.buy = buyRules;
    temp.sell = sellRules;
    console.log(temp);
    setRules(temp);
    setStage(2);
  }

  const addDetails = (strategyName, positionSize) => {
    let asDict = {'name': strategyName,
        'positionSize': parseInt(positionSize),
        'indicators': indicators,
        'rules': rules
      };
    setStage(3);
    console.log(asDict);
    setAsDict(asDict);
  }
  
  const create = () => {
    protectedFetch("/api/create_strategy", {
      method: "POST",
      body: JSON.stringify(asDict)}).then(() => {
        setRedirect(true);
      });
  }
  
  return ( 
    redirectToStrategies ? <Navigate to="/strategies"></Navigate> : 
    <CenteredPageContainer>
      <Grid>
          { stage === 0 ? <IndicatorSelector onComplete={chooseIndicators}/> : null}
          { stage === 1 ? <RuleMaker indicators={indicators} onComplete={addRules}/> : null}
          { stage === 2 || stage == 3 ? <StrategyDetails onComplete={addDetails} /> : null }
          { stage === 3 ? <Button color="success" onClick={create}>Create Strategy</Button> : null}
      </Grid>
    </CenteredPageContainer>
  );
}
 
export default StrategyWriter;