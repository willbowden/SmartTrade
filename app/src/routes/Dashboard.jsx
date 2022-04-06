import React from "react";
import {useState, useEffect} from 'react';
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import { Grid, Typography, Card, CardConten } from '@mui/material';
import HoldingsTable from "../components/holdingsTable.jsx";
import GenericChart from "../components/genericChart.jsx";
import protectedFetch from "../auth/protectedFetch.js";


function Dashboard() {
  
  return ( 
    <CenteredPageContainer>
      <Grid item xs={12}>
        <Typography variant="h1">Welcome</Typography>
      </Grid>
      <Grid item xs={4} >
        <HoldingsTable />
      </Grid>
    </CenteredPageContainer>
  );
}
 
export default Dashboard;