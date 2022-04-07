import React from 'react';
import {useState, useEffect} from 'react';
import protectedFetch from "../auth/protectedFetch.js";
import { Typography } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { fromUnixTime } from "date-fns";
import CenteredPageContainer from "../components/centeredPageContainer";

const TradeList = () => {
    const [tradeHistory, setTradeHistory] = useState(null);
    const columns = [
        { field: 'id', headerName: 'ID', width: 50},
        { field: 'timestamp', headerName:'Date', flex: 1},
        { field: 'symbol', headerName: 'Pair', flex: 0.25},
        { field: 'type', headerName: 'side', flex: 0.25},
        { field: 'quantity', headerName: 'Amount', flex: 0.5},
        { field: 'price', headerName: 'Price', flex: 0.25}
    ];


    useEffect(() => {
      protectedFetch('/api/get_user_trades').then((results) => {
        results = JSON.parse(results);
        let id = 0;
        let newOrderHistory = [];
        results.forEach((row) => {
          let newRow = row;
          newRow.id = id;
          newRow.timestamp = fromUnixTime(newRow.timestamp / 1000);
          newOrderHistory.push(newRow);
          id += 1;
        })
        setTradeHistory(newOrderHistory);
        console.log(newOrderHistory);
      })
    }, [])

    return (
        <CenteredPageContainer>
            { tradeHistory === null ? <Typography variant="h4">We're calculating your trade history.</Typography> 
            : 
            <DataGrid
            rows={tradeHistory}
            columns={columns}
            autoHeight={true}
            pageSize={15}
            rowsPerPageOptions={[30]}
            checkboxSelection
            disableSelectionOnClick
            />
            }
        </CenteredPageContainer>
    )
}

export default TradeList;