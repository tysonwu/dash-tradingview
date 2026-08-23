import React from 'react';
import {
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
    createOptionsChart,
} from 'lightweight-charts';
import type {DeepPartial, PriceChartOptions} from 'lightweight-charts';

import ChartCore from '../core/chart';
import type {ChartKind, ChartProps, PaneSpec, SeriesSpec} from '../core/types';

/**
 * Series names accepted by the `series` prop. An options chart draws the same
 * series types a time chart does; only what the horizontal axis measures
 * differs.
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

const KIND: ChartKind<number> = {
    name: 'Tvlwo',
    create: (container, options) =>
        createOptionsChart(container, options as DeepPartial<PriceChartOptions>),
    definitions: DEFINITIONS,
};

/**
 * Defaults for the object-valued props. These are module-level so their
 * identity is stable across renders: an inline `{}` or `[]` in the
 * destructuring pattern allocates afresh every render, which would re-fire the
 * effects downstream, and those effects write read-back props, so it would loop.
 */
const EMPTY_CHART_OPTIONS: DeepPartial<PriceChartOptions> = {};
const EMPTY_SERIES: SeriesSpec<number, SeriesTypeName>[] = [];
const EMPTY_PANE_OPTIONS: PaneSpec[] = [];

type Props = ChartProps<number, SeriesTypeName> & {
    /**
     * Object containing all chart options. Mirrors the `PriceChartOptions`
     * interface of the underlying charting library, which is the ordinary chart
     * options object with one addition: `localization.precision` sets how many
     * decimal places the horizontal axis labels carry.
     *
     * There is no `timeScale.tickMarkFormatter` here. That option belongs to
     * time charts; the horizontal axis is formatted through
     * `localization.precision` instead. Every other `timeScale` option applies
     * unchanged, including `barSpacing`, `minBarSpacing`, the borders and the
     * conflation group.
     *
     * Option values that must be functions, such as
     * `localization.priceFormatter`, are given as the string name of a function
     * registered on `window.dashTvlwcFunctions`.
     */
    chartOptions: DeepPartial<PriceChartOptions>;
};

/**
 * Tradingview Lightweight Chart on a price axis, for option payoff and
 * volatility curves. Points carry `time` as a number, which the chart reads as
 * a position on the horizontal price scale rather than as a moment, so a strike
 * of 105.5 is written `{'time': 105.5, 'value': ...}`. Points must still be
 * unique and ascending in `time`.
 */
const Tvlwo = ({
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
    <ChartCore<number, SeriesTypeName>
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

export default Tvlwo;
