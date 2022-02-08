import React, {useState, useEffect} from "react";
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import { Grid, Button } from '@mui/material';
import IndicatorSelector from "../components/indicatorSelector.jsx";
import RuleMaker from "../components/ruleMaker.jsx";
import StrategyDetails from '../components/strategyDetails.jsx';
import protectedFetch from '../auth/protectedFetch.jsx';
import { Navigate } from 'react-router-dom';

function StrategyWriter(props) {
  const [stage, setStage] = useState(0);
  const [indicators, setIndicators] = useState(props.state.indicators || null);
  const [rules, setRules] = useState(props.state.rules || null);
  const [asDict, setAsDict] = useState({})
  const [allowSubmit, setAllowSubmit] = useState(false);

  useEffect(() => {
    if (asDict !== {}) {
      setAllowSubmit(true);
    }
  }, [asDict])

  const chooseIndicators = (chosen) => {  
    setIndicators(chosen);
    setStage(1);
  }

  const addRules = (buyRules, sellRules) => {
    let temp = rules;
    temp.buy = buyRules;
    temp.sell = sellRules;
    setRules(temp)
    setStage(2);
  }

  const addDetails = (strategyName, balance) => {
    let asDict = {'name': strategyName,
        'startingBalance': balance,
        'indicators': indicators,
        'rules': rules
      };
    setStage(3);
    setAsDict(asDict);
  }
  
  const create = () => {
    protectedFetch("/api/create_strategy", {
      method: "POST",
      body: JSON.stringify(asDict)}).then(() => {
        return <Navigate to="/strategies"></Navigate>
      });
  }
  
  return ( 
    <CenteredPageContainer>
      <Grid>
          { stage === 0 ? <IndicatorSelector onComplete={chooseIndicators}/> : null}
          { stage === 1 ? <RuleMaker indicators={indicators} onComplete={addRules}/> : null}
          { stage == 2 ? <StrategyDetails onComplete={addDetails} /> : null }
          { stage == 3 ? <Button disabled={allowSubmit} color="success" onClick={create}>Create Strategy</Button> : null}
      </Grid>
    </CenteredPageContainer>
  );
}
 
export default StrategyWriter;