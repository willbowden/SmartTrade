import React, { useState, useRef, useLayoutEffect } from "react";
import "../App.css";
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import protectedFetch from "../auth/protectedFetch";

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
    console.log(this.props.test);
    const token_header = JSON.parse(localStorage.getItem('REACT_TOKEN_AUTH_KEY'));
    const token = token_header.access_token
    let x = am4core.create("chartdiv", am4charts.XYChart);

    x.paddingRight = 20;

    let dateAxis = x.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.baseInterval = {
        "timeUnit": "hour",
        "count": 1
    }
    dateAxis.dateFormatter = new am4core.DateFormatter();
    dateAxis.dateFormatter.dateFormat = "i";

    let valueAxis = x.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.renderer.minWidth = 35;

    var series = x.series.push(new am4charts.CandlestickSeries());
    series.dataFields.dateX = "timestamp";
    series.dataFields.valueY = "close";
    series.dataFields.openValueY = "open";
    series.dataFields.lowValueY = "low";
    series.dataFields.highValueY = "high";
    series.tooltipText = "Open: ${openValueY.value}[/]\nLow: ${lowValueY.value}[/]\nHigh: ${highValueY.value}[/]\nClose: ${valueY.value}[/]";
    x.cursor = new am4charts.XYCursor()
    x.cursor.behaviour = "panX";

    chart.current = x;

    return () => {
      x.dispose();
    };
  }, []);
  
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
    <div className="centered-div">
      {loading ? null : null}
      <form>
        <label>Symbol:</label> {/* Form for entering info */}
        <input
          type="text"
          value={symbol}
          onChange={(e) => {
            setSymbol(e.target.value);
          }}
        ></input>
      </form>
      <form>
        <label>Timeframe:</label> {/* Form for entering info */}
        <input
          type="text"
          value={timeframe}
          onChange={(e) => {
            setTimeframe(e.target.value);
          }}
        ></input>
      </form>
      <form>
        <label>Start Date:</label> {/* Form for entering info */}
        <input
          type="text"
          value={startDate}
          onChange={(e) => {
            setStartDate(e.target.value);
          }}
        ></input>
      </form>
      <div id="chartdiv" style={{ width: "100%", height: "500px" }}></div>
      <input
        className="button"
        type="button"
        value="Test"
        onClick={sendRequest}
      ></input>
    </div>
  );
}

export default CandlestickChart;
