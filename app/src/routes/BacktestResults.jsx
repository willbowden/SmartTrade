import React, { useEffect } from "react";
import '../App.css';
import {useState} from 'react';
import CenteredPageContainer from "../components/centeredPageContainer";
import CandlestickChart from '../components/candlestickChart.jsx';
import { Grid, Typography, Card, CardContent} from '@mui/material';
import {red, teal, cyan} from '@mui/material/colors';
import { DataGrid } from '@mui/x-data-grid';

const columns = [
  { field: 'id', headerName: 'ID', flex: 1},
  { field: 'timestamp', headerName: 'Date', flex: 1, width: 200 },
  {
    field: 'symbol',
    headerName: 'Currency',
    flex: 1,
    editable: false,
  },
  {
    field: 'side',
    headerName: 'Side',
    flex: 1,
    editable: true,
  },
  {
    field: 'quantity',
    headerName: 'Quantity',
    type: 'number',
    flex: 1,
    editable: false,
  },
  {
    field: 'price',
    headerName: 'Price',
    type: 'number',
    flex: 1,
    editable: false,
  },
  {
    field: 'profit',
    headerName: 'Profit',
    type: 'number',
    flex: 1,
    editable: false,
  }
];
 
function BacktestResults(props) {
  const [loading, setLoading] = useState(false);
  const [selectedGraph, setSelectedGraph] = useState("");
  const [profitTextColour, setProfitColour] = useState(teal[500]);

  useEffect(() => {
    setProfitColour(props.results.profit > 0 ? teal[500] : red[500]);
    console.log(props.results.orderHistory)
  }, [])

  const roundTo2 = (num) => {
    return Math.round((num + Number.EPSILON) * 100) / 100
  }

  return (
    props.results && 
      <CenteredPageContainer>
      <Grid item xs={12}>
        <Typography variant="h2">Backtest Results</Typography>
      </Grid>
      <Grid item xs={4}>
        <Card>
          <CardContent>
            <Typography variant="h3">Profit</Typography>
            <Typography variant="h4" color={profitTextColour}>${roundTo2(props.results.profit)}</Typography>
            <Typography variant="body1" color={profitTextColour}>{roundTo2(props.results.profitPercent)}%</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={4}>
        <Card>
          <CardContent>
            <Typography variant="h3">Number Of Orders</Typography>
            <Typography variant="h4" color={cyan[500]}>{props.results.numOrders}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12}>
        <DataGrid
          rows={props.results.orderHistory}
          columns={columns}
          autoHeight={true}
          pageSize={5}
          rowsPerPageOptions={[5]}
          checkboxSelection
          disableSelectionOnClick
        />
      </Grid>
    </CenteredPageContainer>
  );
}
 
export default BacktestResults;