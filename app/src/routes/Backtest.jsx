import React from "react";
import '../App.css';
import { Typography } from '@mui/material';
import CenteredPageContainer from "../components/centeredPageContainer";
import UserStrategies from './UserStrategies.jsx';
 
class Backtest extends React.Component {
  render() {
    return (
      <CenteredPageContainer>
        <UserStrategies></UserStrategies>
      </CenteredPageContainer>
    );
  }
}
 
export default Backtest;