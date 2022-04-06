import React, { useState, useEffect } from "react";
import Chart from 'kaktana-react-lightweight-charts';
import protectedFetch from "../auth/protectedFetch";
import { Box, Stack, TextField, Button, CircularProgress } from '@mui/material';
import CenteredPageContainer from "./centeredPageContainer";
import { Navigate } from 'react-router-dom';

function GenericChart(props) {
  const [options, setOptions] = useState({layout: {
    backgroundColor: '#131722',
    textColor: 'rgba(255, 255, 255, 0.9)',
  }, 
  timeScale: {
    timeVisible: true,
    secondsVisible: false,
  },
  grid: {
    vertLines: {
      color: '#292929',
    },
    horzLines: {
      color: '#292929',
    },
  }});
  
  return (
    <CenteredPageContainer>
      <Box sx={{width: '100vw'}}>
        <Chart options={props.options} candlestickSeries={props.candlestickSeries} lineSeries={props.lineSeries} autoWidth={props.autoWidth} width={props.height} height={props.height} />
      </Box>
    </CenteredPageContainer>
  );
}

export default GenericChart;
