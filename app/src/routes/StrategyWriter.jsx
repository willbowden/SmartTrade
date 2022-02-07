import React from "react";
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import { Grid } from '@mui/material';
import IndicatorSelector from "../components/indicatorSelector.jsx";


function StrategyWriter() {
  
  return ( 
    <CenteredPageContainer>
      <Grid>
          <IndicatorSelector></IndicatorSelector>
      </Grid>
    </CenteredPageContainer>
  );
}
 
export default StrategyWriter;