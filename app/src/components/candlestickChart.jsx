import React, { useState, useEffect } from "react";
import protectedFetch from "../auth/protectedFetch";
import { Box, Stack, TextField, Button, CircularProgress } from '@mui/material';
import CenteredPageContainer from "./centeredPageContainer";
import { Navigate } from 'react-router-dom';
import GenericChart from "./genericChart";

function CandlestickChart(props) {
  const [symbol, setSymbol] = useState("ETH/USDT");
  const [timeframe, setTimeframe] = useState("1h");
  const [startDate, setStartDate] = useState(1634304616000);
  const [loading, setLoading] = useState(false);
  const [candlestickSeries, setCandleStickSeries] = useState([]);
  const [lineSeries, setLineSeries] = useState([]);
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
  const [shouldRedirect, setShouldRedirect] = useState(false);
  const overlaps = ['ma', 'ema']

  const sendRequest = (e) => {
    // Send a request to the api endpoint of choice
    e.preventDefault();
    setLoading(true);
    let payload = {
      symbol: symbol,
      timeframe: timeframe,
      startDate: startDate,
      requiredIndicators: props.indicators
    };

    protectedFetch("/api/test_candlestick_chart", {
      method: "POST",
      body: JSON.stringify(payload),
    }).then((data) => {
      if (data.response === 'Error') {
        setShouldRedirect(true);
      }
      setLoading(false);
      let asArray = JSON.parse(data);
      let temp = [...candlestickSeries];
      temp.push({data: asArray});
      setCandleStickSeries(temp);

      props.indicators.forEach((ind) => {
        if (ind.plot) {
            let tempSeries = [];
            ind.plot.objects.forEach((obj) => {
                var newArray = [];
                var name = ind.name + "_" + obj.name;
                if (overlaps.includes(ind.name)) {
                    name = name + "_" + ind.arguments['timeperiod'];
                }

                asArray.forEach((row) => {
                    newArray.push({time: row.time, value: row[name]})
                })

                tempSeries.push({options: {
                    color: obj.colour,
                    lineWidth: obj.linewidth
                }, data: newArray});
                if (obj.type === 'LineSeries') { 
                    let oldSeries = [...lineSeries];
                    let newSeries = oldSeries.concat(tempSeries);
                    setLineSeries(newSeries);
                }
            })
        }
      })
    });
  };

  useEffect(() => {
      console.log(candlestickSeries);
  }, [candlestickSeries])

  return (
    <CenteredPageContainer>
      { shouldRedirect ? <Navigate to="/login" /> : null}
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
        <GenericChart options={options} candlestickSeries={candlestickSeries} lineSeries={lineSeries} autoWidth={true} height={500} />
      </Box>
      </Stack>
        }
    </CenteredPageContainer>
  );
}

export default CandlestickChart;
