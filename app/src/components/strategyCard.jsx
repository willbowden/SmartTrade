import React, {useState} from "react";
import {Card, CardActions, CardContent, Typography, Button} from '@mui/material';

export default function StrategyCard(props) {
    return <Card>
        <CardContent>
            <Typography variant="h6">{props.name}</Typography>
            <Typography variant="body2">Win Rate: {props.winrate}</Typography>
            <Typography variant="body2">Average Return: {props.return}</Typography>
        </CardContent>
        <CardActions disableSpacing>
            <Button onClick={() => {props.selectStrategy(props.name)}} size="small">Backtest</Button>
            <Button color="error" onClick={() => {props.deleteStrategy(props.name)}} size="small">Delete</Button>
        </CardActions>
    </Card>
}