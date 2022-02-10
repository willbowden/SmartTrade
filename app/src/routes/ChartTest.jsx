import React, {useState} from 'react';
import CandlestickChart from '../components/candlestickChart.jsx';
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import IndicatorSelector from "../components/indicatorSelector.jsx";

function ChartTest() {
    const [indicators, setIndicators] = useState([]);

    const chooseIndicators = (chosen) => {
        setIndicators(chosen);
        console.log(chosen);
      }

    return(
        <CenteredPageContainer>
            <IndicatorSelector onComplete={chooseIndicators}></IndicatorSelector>
            <CandlestickChart indicators={indicators}></CandlestickChart>
        </CenteredPageContainer>
    );
}

export default ChartTest;