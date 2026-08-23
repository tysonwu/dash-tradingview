import React from 'react';
import {
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
    createChart,
} from 'lightweight-charts';
import type {ChartOptions, DeepPartial, Time} from 'lightweight-charts';

import ChartCore from '../core/chart';
import type {ChartKind, ChartProps, PaneSpec, SeriesSpec} from '../core/types';

/**
 * Series names accepted by the `series` prop, mapped to the upstream series
 * definitions that `chart.addSeries` expects.
 */
const DEFINITIONS = {
    area: AreaSeries,
    bar: BarSeries,
    baseline: BaselineSeries,
    candlestick: CandlestickSeries,
    histogram: HistogramSeries,
    line: LineSeries,
} as const;

type SeriesTypeName = keyof typeof DEFINITIONS;

const KIND: ChartKind<Time> = {
    name: 'Tvlwc',
    create: (container, options) =>
        createChart(container, options as DeepPartial<ChartOptions>),
    definitions: DEFINITIONS,
};

/**
 * Defaults for the object-valued props. These are module-level so their
 * identity is stable across renders: an inline `{}` or `[]` in the
 * destructuring pattern allocates afresh every render, which would re-fire the
 * effects downstream, and those effects write read-back props, so it would loop.
 */
const EMPTY_CHART_OPTIONS: DeepPartial<ChartOptions> = {};
const EMPTY_SERIES: SeriesSpec<Time, SeriesTypeName>[] = [];
const EMPTY_PANE_OPTIONS: PaneSpec[] = [];

type Props = ChartProps<Time, SeriesTypeName> & {
    /**
     * Object containing all chart options. Mirrors the `ChartOptions` interface
     * of the underlying charting library. Option values that must be functions,
     * such as `localization.priceFormatter` and `timeScale.tickMarkFormatter`,
     * are given as the string name of a function registered on
     * `window.dashTvlwcFunctions`.
     */
    chartOptions: DeepPartial<ChartOptions>;
};

/**
 * Tradingview Lightweight Chart on a time axis. Data points carry `time` as a
 * `YYYY-MM-DD` string, a `{year, month, day}` object, or a UTC timestamp in
 * seconds, and every payload reports times back in the form they were given in.
 */
const Tvlwc = ({
    chartOptions = EMPTY_CHART_OPTIONS,
    series = EMPTY_SERIES,
    paneOptions = EMPTY_PANE_OPTIONS,
    screenshotRequest = 0,
    subscribeCrosshair = false,
    subscribeClick = false,
    subscribeDblClick = false,
    subscribeVisibleRange = false,
    subscribeSize = false,
    reportThrottle = 0,
    width = '100%',
    height = 400,
    ...rest
}: Props) => (
    <ChartCore<Time, SeriesTypeName>
        kind={KIND}
        {...{
            chartOptions,
            series,
            paneOptions,
            screenshotRequest,
            subscribeCrosshair,
            subscribeClick,
            subscribeDblClick,
            subscribeVisibleRange,
            subscribeSize,
            reportThrottle,
            width,
            height,
        }}
        {...rest}
    />
);

export default Tvlwc;
