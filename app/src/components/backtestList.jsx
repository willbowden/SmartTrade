import React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, CircularProgress, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from '@mui/material';


export default function BacktestList(props) {
    
    return (
        <>
        <TableContainer component={Paper} sx={{tableLayout: 'auto'}}>
            <Table>
            <TableHead>
                <Typography variant="h3">Backtests</Typography>
            <TableRow>
                <TableCell>Start Date</TableCell>
                <TableCell>Buy Orders Made</TableCell>
                <TableCell>Sell Orders Made</TableCell>
                <TableCell>Profit</TableCell>
                <TableCell>Action</TableCell>
            </TableRow>
            </TableHead>
            <TableBody>
            { props.backtests ? props.backtests.map((row) => (
                <TableRow key={row.id}>
                <TableCell>{row.startTimestamp}</TableCell>
                <TableCell>{row.numBuys}</TableCell>
                <TableCell>{row.numSells}</TableCell>
                <TableCell>{row.return}</TableCell>
                <TableCell><Button color="error" onClick={() => {props.getResults(row.id)}}>View</Button></TableCell>
                </TableRow> 
            )) : <CircularProgress />}
            </TableBody>
            </Table>
        </TableContainer>
            <Button color="error" onClick={() => {props.hide()}}>Back</Button>
        </>
    )
}