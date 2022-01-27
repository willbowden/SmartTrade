import React, { useState, useRef, useLayoutEffect } from "react";
import "../App.css";
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import protectedFetch from "../auth/protectedFetch";
import { Box, Stack, TextField, Button, CircularProgress } from '@mui/material';
import CenteredPageContainer from "./centeredPageContainer";

am4core.options.onlyShowOnViewport = true;

function CandlestickChart(props) {
  const chart = useRef(null);
  const [symbol, setSymbol] = useState("ETH/USDT");
  const [timeframe, setTimeframe] = useState("1h");
  const [startDate, setStartDate] = useState(1634304616000);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const config = { candleType: "candles", requiredIndicators: [] };

  useLayoutEffect(() => {
    console.log(props.test);
    let x = am4core.create("chartdiv", am4charts.XYChart);

    x.paddingRight = 20;
    x.legend = new am4charts.Legend();
    x.legend.markers.template.disabled = true;

    let dateAxis = x.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.baseInterval = {
        "timeUnit": "hour",
        "count": 1
    }
    dateAxis.dateFormatter = new am4core.DateFormatter();
    dateAxis.dateFormatter.dateFormat = "i";
    dateAxis.renderer.stroke = '#ffffff';
    dateAxis.renderer.fill = "#ffffff";

    let valueAxis = x.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.renderer.minWidth = 35;

    var series = x.series.push(new am4charts.CandlestickSeries());
    series.dataFields.dateX = "timestamp";
    series.dataFields.valueY = "close";
    series.dataFields.openValueY = "open";
    series.dataFields.lowValueY = "low";
    series.dataFields.highValueY = "high";
    series.legendSettings.itemValueText = "[bold]{valueY}[/bold]";
    x.cursor = new am4charts.XYCursor()
    x.cursor.behaviour = "panX";

    chart.current = x;

    return () => {
      x.dispose();
    };
  });
  
  useLayoutEffect(() => {
    chart.current.data = result;
}, [result]);

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
      setResult(asArray);
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
