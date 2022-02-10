import React from "react";
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import { Grid } from '@mui/material';
import HoldingsTable from "../components/holdingsTable.jsx";


function Dashboard() {
  
  return ( 
    <CenteredPageContainer>
      <Grid item xs={4} >
        {/*<HoldingsTable />*/}
      </Grid>
    </CenteredPageContainer>
  );
}
 
export default Dashboard;