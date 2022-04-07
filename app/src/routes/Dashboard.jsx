import React from "react";
import {useState} from 'react';
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import { Grid, Typography } from '@mui/material';
import HoldingsTable from "../components/holdingsTable.jsx";
import TradeList from "../components/tradeList.jsx";


function Dashboard() {  
  return ( 
    <CenteredPageContainer>
      <Grid item xs={12}>
        <Typography variant="h1">Welcome</Typography>
      </Grid>
      <Grid item xs={4} >
        <HoldingsTable />
      </Grid>
      <Grid item xs={12} sx={{width: '90%'}}>
        <TradeList></TradeList>
      </Grid>
    </CenteredPageContainer>
  );
}
 
export default Dashboard;