import React from "react";
import {useState, useEffect} from 'react';
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import { Grid, Typography, Card, CardContent } from '@mui/material';
import HoldingsTable from "../components/holdingsTable.jsx";
import GenericChart from "../components/genericChart.jsx";
import protectedFetch from "../auth/protectedFetch.js";


function Dashboard() {
  const [valueData, setValueData] = useState([])
  const [waitingForData, setWaitingForData] = useState(true);

  useEffect(() => {
    protectedFetch('/api/get_user_trades').then((results) => {
      // const lineSeries = [{data: results}];
      // setValueData(lineSeries);
      // setWaitingForData(false);
      console.log(results);
    })
  }, [])
  
  return ( 
    <CenteredPageContainer>
      <Grid item xs={12}>
        <Typography variant="h1">Welcome</Typography>
      </Grid>
      <Grid item xs={4} >
        {/* <HoldingsTable /> */}
      </Grid>
      <Grid item xs={8}>
        { waitingForData ? <Typography variant="h4">We're calculating your trade history.</Typography> 
        : <GenericChart lineSeries={valueData} autoWidth={true} height={300}></GenericChart>}
      </Grid>
    </CenteredPageContainer>
  );
}
 
export default Dashboard;