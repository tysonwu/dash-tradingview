import React, {useEffect, useRef} from 'react';
import {createChart} from 'lightweight-charts';
import type {ChartOptions, DeepPartial, IChartApi} from 'lightweight-charts';

type Props = {
    /**
     * The ID of this component.
     */
    id?: string;

    /**
     * Object containing all chart options. Mirrors the `ChartOptions` interface
     * of the underlying charting library.
     */
    chartOptions?: DeepPartial<ChartOptions>;

    /**
     * Sets width of the parent div of the chart.
     */
    width?: string | number;

    /**
     * Sets height of the parent div of the chart.
     */
    height?: string | number;

    /**
     * Dash-assigned callback that fires when a prop changes.
     */
    setProps?: (props: Record<string, unknown>) => void;
};

/**
 * Tradingview Lightweight Chart object
 */
const Tvlwc = ({id, chartOptions = {}, width = '100%', height = 400}: Props) => {
    const containerRef = useRef<HTMLDivElement>(null);
    const chartRef = useRef<IChartApi | null>(null);

    // The chart instance outlives renders: it is created once against the
    // container and disposed on unmount.
    useEffect(() => {
        if (!containerRef.current) {
            return undefined;
        }
        chartRef.current = createChart(containerRef.current, {
            autoSize: true,
            ...chartOptions,
        });
        return () => {
            chartRef.current?.remove();
            chartRef.current = null;
        };
    }, []);

    // `autoSize` handles container resizing, so option changes are applied in
    // place rather than by recreating the chart.
    useEffect(() => {
        chartRef.current?.applyOptions(chartOptions);
    }, [chartOptions]);

    return <div id={id} ref={containerRef} style={{width, height}} />;
};

export default Tvlwc;
