import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { createChart } from 'lightweight-charts';


/**
 * Tradingview Lightweight Chart object
 */

const Tvlwc = props => {

    const {
        id, 
        data,
        chartOptions,
    } = props;
    const chartContainerRef = useRef();

    useEffect(
        () => {
            const chart = createChart(chartContainerRef.current, chartOptions);
            
            const handleResize = () => {
                chart.applyOptions({ width: chartContainerRef.current.clientWidth });
            };
            chart.timeScale().fitContent();

            const newSeries = chart.addCandlestickSeries();
            newSeries.setData(data);

            window.addEventListener('resize', handleResize);

            return () => {
                window.removeEventListener('resize', handleResize);
                chart.remove();
            };
        },
        [data, chartOptions]
    );

    return (
        <div id={id} ref={chartContainerRef}></div>
    );        
}

Tvlwc.defaultProps = {};

Tvlwc.propTypes = {
    /**
     * The ID of this component
     */
    id: PropTypes.string,

    /**
     * The data for the series
     */
    data: PropTypes.array,

    /**
     * Object containing all chart options
     * See https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions for possible options
     */
    chartOptions: PropTypes.object,

    // setProps: PropTypes.func
};

export default Tvlwc;