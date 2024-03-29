import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Backtest from './routes/Backtest';
import Dashboard from './routes/Dashboard';
import Login from './routes/Login';
import Register from './routes/Register';
import APITest from './routes/APITest';
import ChartTest from './routes/ChartTest';
import PrivateRoute from './auth/protectedRoute';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import StrategyWriter from './routes/StrategyWriter';

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  }
});

ReactDOM.render(
  <ThemeProvider theme={darkTheme}>
    <div className="fullsize">
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<App />}>
          <Route exact path='/dashboard' element={<PrivateRoute />}>
              <Route exact path='/dashboard' element={<Dashboard />}/>
          </Route>
          <Route exact path='/strategy_writer' element={<PrivateRoute />}>
            <Route exact path="/strategy_writer" element={<StrategyWriter />}/>
          </Route>
          <Route exact path='/chart' element={<PrivateRoute />}>
            <Route exact path='/chart' element={<ChartTest />}/>
          </Route>
          <Route exact path='/api_test' element={<PrivateRoute />}>
              <Route exact path='/api_test' element={<APITest />}/>
          </Route>
          <Route exact path="/backtest" element={<PrivateRoute />}>
            <Route path="/backtest" element={<Backtest />} />
          </Route>
          <Route exact path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Route>
      </Routes>
    </BrowserRouter>
    </div>
  </ThemeProvider>,
  document.getElementById('root')
);