import React from "react";
import '../App.css';
import { Typography } from '@mui/material';
import CenteredPageContainer from "../components/centeredPageContainer";
 
class Backtest extends React.Component {
  render() {
    return (
      <CenteredPageContainer>
        <Typography variant="h1">Backtesting Page</Typography>
      </CenteredPageContainer>
    );
  }
}
 
export default Backtest;