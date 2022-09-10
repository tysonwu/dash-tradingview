import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { createChart, ColorType } from 'lightweight-charts';

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
                width: chartContainerRef.current.clientWidth,
                height: 300,
            });
            const handleResize = () => {
                chart.applyOptions({ width: chartContainerRef.current.clientWidth });
            };
            chart.timeScale().fitContent();

            const newSeries = chart.addAreaSeries({ lineColor: colors.lineColor, topColor: colors.areaTopColor, bottomColor: colors.areaBottomColor });
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
    id: PropTypes.string,
    data: PropTypes.array,
    colors: PropTypes.object,
    // setProps: PropTypes.func
};

export default Tvlwc;