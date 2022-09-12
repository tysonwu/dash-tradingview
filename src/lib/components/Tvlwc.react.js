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
        width,
        height,
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
            
            for (const series of data) {
                let s;
                switch (series.seriesType) {
                    case 'Candlestick':
                        s = chart.addCandlestickSeries(series.seriesOptions);
                        break;
                    case 'Area':
                        s = chart.addAreaSeries(series.seriesOptions);
                        break;
                    default:
                        break;
                    }
                s.setData(series.seriesData);
            };            

            window.addEventListener('resize', handleResize);

            return () => {
                window.removeEventListener('resize', handleResize);
                chart.remove();
            };
        },
        [data, chartOptions]
    );

    return (
        <div id={id} ref={chartContainerRef} style={{height: height, width: width}} />
    );
}

Tvlwc.defaultProps = {
    width: 600,
    height: 400,
};

Tvlwc.propTypes = {
    /**
     * The ID of this component
     */
    id: PropTypes.string,

    /**
     * The data for the series
     */
    data: PropTypes.arrayOf(PropTypes.shape(
        {
            seriesData: PropTypes.arrayOf(PropTypes.object),
            seriesType: PropTypes.oneOf(['Candlestick', 'Area']),
            seriesOptions: PropTypes.object,
        }
    )),
    
    /**
     * Sets width of the parent div of the chart
     */
    width: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),

    /**
     * Sets height of the parent div of the chart
     */
    height: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),

    /**
     * Object containing all chart options
     * See https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions for possible options
     */
    chartOptions: PropTypes.object,

    // setProps: PropTypes.func
};

export default Tvlwc;