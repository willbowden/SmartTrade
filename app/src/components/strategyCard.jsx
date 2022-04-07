import React, {useState} from "react";
import {Card, CardActions, CardContent, Typography, Button} from '@mui/material';

const roundTo2 = (num) => {
    return Math.round((num + Number.EPSILON) * 100) / 100
  }

export default function StrategyCard(props) {
    return <Card>
        <CardContent>
            <Typography variant="h6">{props.name}</Typography>
            <Typography variant="body2">Win Rate: {roundTo2(props.winrate)}</Typography>
            <Typography variant="body2">Average Return: {roundTo2(props.return)}</Typography>
        </CardContent>
        <CardActions disableSpacing>
            <Button onClick={() => {props.selectStrategy(props.name)}} size="small">Backtest</Button>
            <Button onClick={() => {props.viewBacktests(props.name)}} size="small">View</Button>
            <Button color="error" onClick={() => {props.deleteStrategy(props.name)}} size="small">Delete</Button>
        </CardActions>
    </Card>
}