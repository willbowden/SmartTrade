import React from 'react';
import CandlestickChart from '../components/candlestickChart.jsx';
import CenteredPageContainer from '../components/centeredPageContainer.jsx';

function ChartTest() {

    return(
        <CenteredPageContainer>
            <CandlestickChart></CandlestickChart>
        </CenteredPageContainer>
    );
}

export default ChartTest;