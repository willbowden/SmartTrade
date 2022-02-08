import React, {useState} from "react";
import CenteredPageContainer from '../components/centeredPageContainer.jsx';
import { Grid } from '@mui/material';

function StrategyWriter() {
    const [loading, setLoading] = useState(true);
    const [strategies, setStrategies] = useState([]);
  
    return ( 
    <CenteredPageContainer>
        {loading ? null : strategies.map((object, i) => {
            return 
        })}
    </CenteredPageContainer>
    );
}
 
export default StrategyWriter;