import React from 'react';
import {AreaSeries, LineSeries, createYieldCurveChart} from 'lightweight-charts';
import type {
    DeepPartial,
    IChartApiBase,
    YieldCurveChartOptions,
} from 'lightweight-charts';

import ChartCore from '../core/chart';
import type {ChartKind, ChartProps, PaneSpec, SeriesSpec} from '../core/types';

/**
 * Series names accepted by the `series` prop. A yield curve chart supports line
 * and area only; the restriction is the library's, and `addSeries` on
 * `IYieldCurveChartApi` is typed to enforce it.
 */
const DEFINITIONS = {
    area: AreaSeries,
    line: LineSeries,
} as const;

type SeriesTypeName = keyof typeof DEFINITIONS;

const KIND: ChartKind<number> = {
    name: 'Tvlwy',
    create: (container, options) =>
        // `IYieldCurveChartApi` narrows `addSeries` to the two series types
        // above, so it is deliberately not assignable to the general
        // `IChartApiBase` the core is written against. `definitions` is what
        // enforces the same restriction at runtime: a `series` entry naming
        // anything else is rejected by name, with a message listing the valid
        // names, before it can reach `addSeries`.
        createYieldCurveChart(
            container,
            options as DeepPartial<YieldCurveChartOptions>
        ) as IChartApiBase<number>,
    definitions: DEFINITIONS,
};

/**
 * Defaults for the object-valued props. These are module-level so their
 * identity is stable across renders: an inline `{}` or `[]` in the
 * destructuring pattern allocates afresh every render, which would re-fire the
 * effects downstream, and those effects write read-back props, so it would loop.
 */
const EMPTY_CHART_OPTIONS: DeepPartial<YieldCurveChartOptions> = {};
const EMPTY_SERIES: SeriesSpec<number, SeriesTypeName>[] = [];
const EMPTY_PANE_OPTIONS: PaneSpec[] = [];

type Props = ChartProps<number, SeriesTypeName> & {
    /**
     * Object containing all chart options. Mirrors the `YieldCurveChartOptions`
     * interface of the underlying charting library: the ordinary chart options
     * object plus a `yieldCurve` group of `baseResolution` (the smallest time
     * unit, default 1 month), `minimumTimeRange` (default 120, so ten years are
     * always in view) and `startTimeRange` (default 0).
     *
     * To label the maturity axis, give `localization.timeFormatter` the string
     * name of a function registered on `window.dashTvlwcFunctions`. It receives
     * the maturity in `baseResolution` units and returns the label; without one
     * the axis falls back to `6M` and `5Y` style defaults.
     *
     * `yieldCurve.formatTime` looks like the option for that and is not. The
     * upstream typings declare it, but lightweight-charts 5.2.1 never reads it,
     * so setting it changes nothing. Passing it here logs a warning pointing at
     * `localization.timeFormatter` rather than failing silently.
     *
     * There is no `timeScale.tickMarkFormatter` here either; that option belongs
     * to time charts. Every other `timeScale` option applies unchanged.
     */
    chartOptions: DeepPartial<YieldCurveChartOptions>;
};

/**
 * Tradingview Lightweight Chart on a maturity axis, for yield curves. Points
 * carry `time` as a number of `chartOptions.yieldCurve.baseResolution` units
 * from `startTimeRange`, which defaults to months from zero, so a ten-year
 * point is written `{'time': 120, 'value': 4.3}`. The chart spaces maturities
 * by that value rather than evenly, which is what makes the short end of a
 * curve read correctly. Points must be unique and ascending in `time`.
 */
const Tvlwy = ({
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

export default Tvlwy;
