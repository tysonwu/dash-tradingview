import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { createChart, ColorType } from 'lightweight-charts';


/**
 * Tradingview Lightweight Chart object
 */

const Tvlwc = props => {

    const {id, data, colors} = props;
    const chartContainerRef = useRef();

    useEffect(
        () => {
            const chart = createChart(chartContainerRef.current, {
                layout: {
                    background: { type: ColorType.Solid, color: colors.backgroundColor },
                    textColor: colors.textColor,
                },
                grid: {
                    vertLines: false,
                    horzLines: false,
                },
                width: 1000,
                height: 800,
            });
            
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
        [data, colors.backgroundColor, colors.lineColor, colors.textColor, colors.areaTopColor, colors.areaBottomColor]
    );

    return (
        <div>
            <h1>Hello!!!!</h1>
            <div id={id} ref={chartContainerRef}></div>
        </div>
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
     * An object containing colors properties
     */
    colors: PropTypes.object,

    // setProps: PropTypes.func
};

export default Tvlwc;