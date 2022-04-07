import React from 'react';
import { useState, useEffect } from 'react';
import protectedFetch from "../auth/protectedFetch.js";
import { Button, CircularProgress, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material';
import {Navigate} from 'react-router-dom'

export default function HoldingsTable() {
    const [holdings, setHoldings] = useState(null);
    const [refresh, setRefresh] = useState(false);
    const [totalValue, setTotalValue] = useState(0);
    const [shouldRedirect, setRedirect] = useState(false);


    useEffect(() => {
        protectedFetch('/api/get_user_holdings').then(result => {
        let asArray = []
        for (const [key, value] of Object.entries(result)) {
            if (key !== 'totalValue') {
            asArray.push({asset: key, quantity: value.balance, value: value.value})
            }
        }
        asArray.sort(function(first, second) {
            return second.value - first.value;
        });
        setHoldings(asArray);
        }).catch((err) => {
            setRedirect(true);
        })
    }, [refresh])

    function onRefreshClick(e) {
        e.preventDefault();
        refresh ? setRefresh(false) : setRefresh(true);
        setHoldings(null);
    }

    return (
    <TableContainer component={Paper} sx={{tableLayout: 'auto'}}>
        {shouldRedirect ? <Navigate to='/login' /> : null}
        <Table>
        <TableHead>
            <Typography variant="h3">My Assets: ${totalValue}</Typography>
        <TableRow>
            <TableCell>Asset</TableCell>
            <TableCell>Quantity</TableCell>
            <TableCell>Value</TableCell>
        </TableRow>
        </TableHead>
        <TableBody>
        { holdings ? holdings.map((row) => (
            <TableRow key={row.asset}>
            <TableCell>{row.asset}</TableCell>
            <TableCell>{row.quantity}</TableCell>
            <TableCell>{row.value}</TableCell>
            </TableRow> 
        )) : <CircularProgress />}
        </TableBody>
        </Table>
        <Button variant="contained" onClick={onRefreshClick}>Refresh</Button>
  </TableContainer>)
}