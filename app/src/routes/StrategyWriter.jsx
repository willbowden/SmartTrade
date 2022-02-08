import React, {useState} from "react";
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import { Grid } from '@mui/material';
import IndicatorSelector from "../components/indicatorSelector.jsx";
import RuleMaker from "../components/ruleMaker.jsx";

function StrategyWriter() {
  const [stage, setStage] = useState(0);
  const [indicators, setIndicators] = useState([]);
  const [rules, setRules] = useState({});

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
  
  return ( 
    <CenteredPageContainer>
      <Grid>
          { stage === 0 ? <IndicatorSelector onComplete={chooseIndicators}/> : null}
          { stage === 1 ? <RuleMaker indicators={indicators} onComplete={addRules}/> : null}
      </Grid>
    </CenteredPageContainer>
  );
}
 
export default StrategyWriter;