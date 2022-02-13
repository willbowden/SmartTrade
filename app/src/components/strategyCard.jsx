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
            <Button size="small">Backtest</Button>
        </CardActions>
    </Card>
}