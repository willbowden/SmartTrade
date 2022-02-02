import React, { useState, useRef, useEffect } from "react";
import { createChart } from 'lightweight-charts';
import protectedFetch from "../auth/protectedFetch";
import { Box, Stack, TextField, Button, CircularProgress } from '@mui/material';
import CenteredPageContainer from "./centeredPageContainer";

function CandlestickChart(props) {
  const [mainChart, setChart] = useState(null)
  const [symbol, setSymbol] = useState("ETH/USDT");
  const [timeframe, setTimeframe] = useState("1h");
  const [startDate, setStartDate] = useState(1634304616000);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const config = { candleType: "candles", requiredIndicators: [] };

  useEffect(() => {
    const chart = createChart(document.getElementById('chartdiv'), {layout: {
      backgroundColor: '#131722',
      textColor: 'rgba(255, 255, 255, 0.9)',
    },});
    setChart(chart);
  }, []);

  const sendRequest = (e) => {
    // Send a request to the api endpoint of choice
    e.preventDefault();
    setLoading(true);
    let payload = {
      symbol: symbol,
      timeframe: timeframe,
      startDate: startDate,
      config: config,
    };

    protectedFetch("/api/test_candlestick_chart", {
      method: "POST",
      body: JSON.stringify(payload),
    }).then((data) => {
      setLoading(false);
      let asArray = JSON.parse(data);
      console.log(asArray);
      const candleSeries = mainChart.addCandlestickSeries();
      candleSeries.setData(asArray);

    });
  };

  return (
    <CenteredPageContainer>
      {loading ? <CircularProgress /> : 
      <Stack sx={{display: 'flex', justifyContent: 'center'}}>
      <Box
          component="form"
          sx={{
            '& .MuiTextField-root': { m: 1, width: '25ch' },
            backgroundColor: '#212121',
            borderRadius: 2,
            padding: 3
          }}
          noValidate
          autoComplete="off"
        >
          <TextField label="Symbol" value={symbol} onChange={(e) => setSymbol(e.target.value)} />
          <TextField label="Timeframe" value={timeframe} onChange={(e) => setTimeframe(e.target.value)} />
          <TextField label="Start Date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          <Button variant="contained" color="success" onClick={sendRequest}>Go</Button>
      </Box>
      <Box sx={{width: '100vw'}}>
        <div id="chartdiv" style={{ width: "100%", height: "500px" }}></div>
      </Box>
      </Stack>
        }
    </CenteredPageContainer>
  );
}

export default CandlestickChart;
