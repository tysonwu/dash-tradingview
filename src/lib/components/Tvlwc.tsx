import React, {useEffect, useRef} from 'react';
import {
    AreaSeries,
    BarSeries,
    BaselineSeries,
    CandlestickSeries,
    HistogramSeries,
    LineSeries,
    createChart,
    createSeriesMarkers,
} from 'lightweight-charts';
import type {
    AreaData,
    BarData,
    BaselineData,
    CandlestickData,
    ChartOptions,
    CreatePriceLineOptions,
    DeepPartial,
    HistogramData,
    IChartApi,
    IPriceLine,
    ISeriesApi,
    ISeriesMarkersPluginApi,
    LineData,
    MouseEventParams,
    SeriesMarker,
    SeriesType,
    Time,
    WhitespaceData,
} from 'lightweight-charts';

/**
 * Series type names accepted by the `series` prop, mapped to the upstream
 * series definitions that `chart.addSeries` expects.
 */
const SERIES_DEFINITIONS = {
    area: AreaSeries,
    bar: BarSeries,
    baseline: BaselineSeries,
    candlestick: CandlestickSeries,
    histogram: HistogramSeries,
    line: LineSeries,
} as const;

type SeriesTypeName = keyof typeof SERIES_DEFINITIONS;

/**
 * Global namespace holding user-supplied JavaScript functions. Option values
 * that must be functions are named as strings from Python and looked up here.
 */
const FUNCTION_NAMESPACE = 'dashTvlwcFunctions';

const LOCALIZATION_FUNCTION_KEYS = [
    'priceFormatter',
    'tickmarksPriceFormatter',
    'percentageFormatter',
    'tickmarksPercentageFormatter',
    'timeFormatter',
];

const PRICE_FORMAT_FUNCTION_KEYS = ['formatter', 'tickmarksFormatter'];

type Dict = Record<string, unknown>;

type SeriesDataItem =
    | AreaData<Time>
    | BarData<Time>
    | BaselineData<Time>
    | CandlestickData<Time>
    | HistogramData<Time>
    | LineData<Time>
    | WhitespaceData<Time>;

type SeriesSpec = {
    /**
     * Stable identity for this series. Used to key incremental updates and to
     * key the `crosshair`, `click` and `fullSeriesOptions` payloads.
     */
    id: string;

    /**
     * One of `bar`, `candlestick`, `area`, `baseline`, `line`, `histogram`.
     */
    type: SeriesTypeName;

    /**
     * Data points. Items carrying only `time` are whitespace and render as gaps.
     */
    data: SeriesDataItem[];

    /**
     * Series options. See the `SeriesOptionsCommon` interface of the underlying
     * charting library, plus the options specific to this series type.
     */
    options?: Dict;

    /**
     * Options for the price scale this series is attached to. This is where
     * `scaleMargins` lives; it is not a series option.
     */
    priceScaleOptions?: Dict;

    /**
     * Markers drawn against this series.
     */
    markers?: SeriesMarker<Time>[];

    /**
     * Horizontal price lines drawn against this series.
     */
    priceLines?: CreatePriceLineOptions[];
};

/**
 * Defaults for the object-valued props. These are module-level so their
 * identity is stable across renders: an inline `{}` or `[]` in the
 * destructuring pattern allocates afresh every render, which would re-fire the
 * effects below, and those effects write read-back props, so it would loop.
 */
const EMPTY_CHART_OPTIONS: DeepPartial<ChartOptions> = {};
const EMPTY_SERIES: SeriesSpec[] = [];

type SeriesRecord = {
    api: ISeriesApi<SeriesType>;
    type: SeriesTypeName;
    spec: Partial<SeriesSpec>;
    markersPlugin: ISeriesMarkersPluginApi<Time> | null;
    priceLines: IPriceLine[];
};

/**
 * Whether the chart has ever held data, tracked per chart rather than per
 * series. A per-series flag would skip the range guard whenever a series is
 * added to, or retyped on, a chart the user has already scrolled, throwing away
 * their viewport.
 */
type ChartState = {hasData: boolean};

type Emitter = {
    push: (value: unknown) => void;
    cancel: () => void;
};

/**
 * Coalesces high-frequency emissions. Every write to a Dash prop is a network
 * round trip, so crosshair movement is batched to at most one write per
 * animation frame, or per `throttleMs` when one is given.
 */
function createEmitter(emit: (value: unknown) => void, throttleMs: number): Emitter {
    let pending: unknown = null;
    let hasPending = false;
    let timerId: number | null = null;
    let frameId: number | null = null;

    const flush = () => {
        timerId = null;
        frameId = null;
        if (!hasPending) {
            return;
        }
        hasPending = false;
        const value = pending;
        pending = null;
        emit(value);
    };

    return {
        push(value) {
            pending = value;
            hasPending = true;
            if (timerId !== null || frameId !== null) {
                return;
            }
            if (throttleMs > 0) {
                timerId = window.setTimeout(flush, throttleMs);
            } else {
                frameId = window.requestAnimationFrame(flush);
            }
        },
        cancel() {
            if (timerId !== null) {
                window.clearTimeout(timerId);
            }
            if (frameId !== null) {
                window.cancelAnimationFrame(frameId);
            }
            timerId = null;
            frameId = null;
            pending = null;
            hasPending = false;
        },
    };
}

/**
 * Looks a function up in the global namespace. Absence throws rather than
 * falling back to a default, so a typo surfaces immediately instead of
 * producing a chart that is subtly wrong.
 */
function resolveFunction(name: unknown, path: string): unknown {
    if (typeof name !== 'string') {
        return name;
    }
    const namespace = (window as unknown as Dict)[FUNCTION_NAMESPACE] as Dict | undefined;
    const fn = namespace ? namespace[name] : undefined;
    if (typeof fn !== 'function') {
        throw new Error(
            `Tvlwc: ${path} names '${name}', which is not a function on ` +
                `window.${FUNCTION_NAMESPACE}. Register it from an assets JavaScript file.`
        );
    }
    return fn;
}

function resolveKeys(source: Dict, keys: string[], pathPrefix: string): Dict {
    const out: Dict = {...source};
    for (const key of keys) {
        if (key in out) {
            out[key] = resolveFunction(out[key], `${pathPrefix}.${key}`);
        }
    }
    return out;
}

/**
 * Returns a copy of `chartOptions` with named functions resolved. The prop
 * itself is never mutated.
 */
function resolveChartOptions(chartOptions: DeepPartial<ChartOptions>): DeepPartial<ChartOptions> {
    const source = chartOptions as Dict;
    const out: Dict = {...source};

    if (source.localization) {
        out.localization = resolveKeys(
            source.localization as Dict,
            LOCALIZATION_FUNCTION_KEYS,
            'chartOptions.localization'
        );
    }
    if (source.timeScale && 'tickMarkFormatter' in (source.timeScale as Dict)) {
        out.timeScale = resolveKeys(
            source.timeScale as Dict,
            ['tickMarkFormatter'],
            'chartOptions.timeScale'
        );
    }
    return out as DeepPartial<ChartOptions>;
}

function resolveSeriesOptions(options: Dict | undefined, seriesId: string): Dict {
    if (!options) {
        return {};
    }
    const out: Dict = {...options};
    if (out.priceFormat && typeof out.priceFormat === 'object') {
        out.priceFormat = resolveKeys(
            out.priceFormat as Dict,
            PRICE_FORMAT_FUNCTION_KEYS,
            `series['${seriesId}'].options.priceFormat`
        );
    }
    return out;
}

/**
 * Replaces a series' data while holding the visible range steady.
 *
 * `setData` resets the visible range, which is the classic snap-to-right-edge
 * bug. Capturing and restoring the logical range makes it safe to call on any
 * data change, so reconciliation needs no content heuristics. The range is not
 * restored while the chart is still empty, where fitting to the new data is
 * correct.
 */
function applyData(
    chart: IChartApi,
    state: ChartState,
    record: SeriesRecord,
    data: SeriesDataItem[]
): void {
    const range = state.hasData ? chart.timeScale().getVisibleLogicalRange() : null;
    record.api.setData(data);
    state.hasData = state.hasData || data.length > 0;
    if (range) {
        chart.timeScale().setVisibleLogicalRange(range);
    }
}

function applyMarkers(record: SeriesRecord, markers: SeriesMarker<Time>[]): void {
    if (record.markersPlugin) {
        record.markersPlugin.setMarkers(markers);
        return;
    }
    if (markers.length === 0) {
        return;
    }
    record.markersPlugin = createSeriesMarkers(record.api, markers);
}

/**
 * Price lines have no diffing API, so survivors are removed and recreated.
 * They are few enough that tracking identity would cost more than it saves.
 *
 * Handles are recorded as they are created rather than assigned in one go at
 * the end. `createPriceLine` throws on a malformed entry, and an assignment
 * that never lands would leave the record holding removed handles while the
 * lines created before the throw stayed on the chart, untrackable and
 * unremovable.
 */
function applyPriceLines(record: SeriesRecord, priceLines: CreatePriceLineOptions[]): void {
    for (const line of record.priceLines) {
        record.api.removePriceLine(line);
    }
    record.priceLines = [];
    for (const options of priceLines) {
        record.priceLines.push(record.api.createPriceLine(options));
    }
}

/**
 * Whether two spec fields are equivalent.
 *
 * Reference equality alone is not enough here. Dash deserializes props from
 * JSON on every callback response, so when the `series` prop changes at all,
 * every object nested inside it is a fresh reference, including the ones whose
 * contents are identical. A reference check would therefore re-apply every
 * option, rebuild every marker and recreate every price line on a data-only
 * update, and would report a series-options read-back to the server each time.
 *
 * The reference check stays as the fast path. Falling back to a serialised
 * comparison is only worthwhile for the small fields; `data` is compared by
 * reference alone, because a series can hold hundreds of thousands of points
 * and replacing it is the expected outcome of a data change anyway.
 */
function sameValue(a: unknown, b: unknown): boolean {
    if (a === b) {
        return true;
    }
    if (a === undefined || b === undefined) {
        return false;
    }
    return JSON.stringify(a) === JSON.stringify(b);
}

function applySpec(
    chart: IChartApi,
    state: ChartState,
    record: SeriesRecord,
    spec: SeriesSpec
): boolean {
    const previous = record.spec;
    let optionsChanged = false;

    if (!sameValue(previous.options, spec.options)) {
        record.api.applyOptions(resolveSeriesOptions(spec.options, spec.id));
        optionsChanged = true;
    }
    if (!sameValue(previous.priceScaleOptions, spec.priceScaleOptions) && spec.priceScaleOptions) {
        record.api.priceScale().applyOptions(spec.priceScaleOptions);
        optionsChanged = true;
    }
    if (previous.data !== spec.data) {
        applyData(chart, state, record, spec.data || []);
    }
    if (!sameValue(previous.markers, spec.markers)) {
        applyMarkers(record, spec.markers || []);
    }
    if (!sameValue(previous.priceLines, spec.priceLines)) {
        applyPriceLines(record, spec.priceLines || []);
    }
    record.spec = spec;
    return optionsChanged;
}

/**
 * Brings the chart's series in line with the `series` prop by id: creates new
 * ones, removes departed ones, and applies changes to survivors in place.
 * Replaces the teardown-and-rebuild approach, which re-ran `setData` for every
 * series on any change to any series.
 */
function reconcileSeries(
    chart: IChartApi,
    state: ChartState,
    records: Map<string, SeriesRecord>,
    series: SeriesSpec[]
): boolean {
    // Validation runs over the whole list before anything is mutated. Failing
    // fast is only useful if the failure is atomic: validating inside the
    // mutation loop would leave earlier series applied, later ones missing, and
    // departed ones still on the chart.
    const seen = new Set<string>();
    for (const spec of series) {
        if (typeof spec.id !== 'string' || spec.id === '') {
            throw new Error('Tvlwc: every entry in `series` needs a non-empty string `id`.');
        }
        if (seen.has(spec.id)) {
            throw new Error(
                `Tvlwc: duplicate series id '${spec.id}'. Ids must be unique within \`series\`.`
            );
        }
        seen.add(spec.id);

        if (!SERIES_DEFINITIONS[spec.type]) {
            throw new Error(
                `Tvlwc: series '${spec.id}' has unknown type '${spec.type}'. ` +
                    `Valid types are ${Object.keys(SERIES_DEFINITIONS).join(', ')}.`
            );
        }
    }

    let changed = false;

    for (const spec of series) {
        const definition = SERIES_DEFINITIONS[spec.type];
        let record = records.get(spec.id);
        // A series API cannot change its own type, so a type change recreates.
        if (record && record.type !== spec.type) {
            chart.removeSeries(record.api);
            records.delete(spec.id);
            record = undefined;
            changed = true;
        }
        if (!record) {
            // Options go in at creation rather than through a follow-up
            // applyOptions, so a series carrying `priceScaleId` is never first
            // attached to the default scale and then moved off it.
            record = {
                api: chart.addSeries(definition, resolveSeriesOptions(spec.options, spec.id)),
                type: spec.type,
                spec: {options: spec.options},
                markersPlugin: null,
                priceLines: [],
            };
            records.set(spec.id, record);
            changed = true;
        }
        changed = applySpec(chart, state, record, spec) || changed;
    }

    for (const [id, record] of Array.from(records.entries())) {
        if (!seen.has(id)) {
            // Removing the series disposes its markers and price lines with it.
            chart.removeSeries(record.api);
            records.delete(id);
            changed = true;
        }
    }

    return changed;
}

/**
 * Builds the `crosshair` and `click` payloads. `param.seriesData` is keyed by
 * series API object, which means nothing to Python, so it is re-keyed by the
 * user's series id. Only series that actually have data under the cursor are
 * included.
 */
function buildMouseEvent(param: MouseEventParams<Time>, records: Map<string, SeriesRecord>): Dict {
    const seriesData: Dict = {};
    const price: Dict = {};
    let hoveredSeriesId: string | null = null;

    const hoveredApi = param.hoveredInfo ? param.hoveredInfo.series : undefined;
    const point = param.point;
    records.forEach((record, id) => {
        const item = param.seriesData.get(record.api);
        if (item !== undefined) {
            seriesData[id] = item;
        }
        // The price under the cursor, on each series' own scale. Unlike
        // `seriesData` this is defined between bars, which is what makes
        // click-to-annotate expressible from Python without exposing the
        // coordinate conversions themselves as props.
        if (point) {
            price[id] = record.api.coordinateToPrice(point.y);
        }
        if (hoveredApi && hoveredApi === record.api) {
            hoveredSeriesId = id;
        }
    });

    return {
        time: param.time === undefined ? null : param.time,
        logical: param.logical === undefined ? null : param.logical,
        paneIndex: param.paneIndex === undefined ? null : param.paneIndex,
        point: point || null,
        seriesData,
        price,
        hoveredSeriesId,
        hoveredObjectId: param.hoveredInfo ? param.hoveredInfo.objectId : null,
    };
}

type Props = {
    /**
     * The ID of this component.
     */
    id?: string;

    /**
     * Object containing all chart options. Mirrors the `ChartOptions` interface
     * of the underlying charting library. Option values that must be functions,
     * such as `localization.priceFormatter`, are given as the string name of a
     * function registered on `window.dashTvlwcFunctions`.
     */
    chartOptions: DeepPartial<ChartOptions>;

    /**
     * The series drawn on this chart, each carrying its own id, type, data,
     * options, markers and price lines.
     */
    series: SeriesSpec[];

    /**
     * Whether to report crosshair movement through the `crosshair` prop. Off by
     * default: every report is a network round trip, and crosshair movement
     * fires on every mouse move.
     */
    subscribeCrosshair?: boolean;

    /**
     * Whether to report chart clicks through the `click` prop.
     */
    subscribeClick?: boolean;

    /**
     * Whether to report time scale range changes through `visibleRange` and
     * `visibleLogicalRange`. Off by default: these fire continuously while
     * panning and zooming.
     */
    subscribeVisibleRange?: boolean;

    /**
     * Whether to report scale dimensions through `timeScaleWidth`,
     * `timeScaleHeight` and `priceScaleWidth`. Off by default: `autoSize`
     * drives these from a resize observer, so they fire every frame while the
     * window is being dragged.
     */
    subscribeSize?: boolean;

    /**
     * Milliseconds to coalesce reports over, applied to every `subscribe*`
     * stream. Zero batches to one report per animation frame.
     */
    reportThrottle?: number;

    /**
     * Sets width of the parent div of the chart.
     */
    width?: string | number;

    /**
     * Sets height of the parent div of the chart.
     */
    height?: string | number;

    /**
     * Crosshair position; read-only. Carries `time`, `logical`, `paneIndex`,
     * `point`, `seriesData` and `price` keyed by series id, `hoveredSeriesId`
     * and `hoveredObjectId`. `seriesData` holds whole data points and is
     * present only for series with data under the cursor; `price` is the price
     * at the cursor on each series' own scale and is defined between bars too.
     * Written only when `subscribeCrosshair` is true.
     */
    crosshair?: Dict;

    /**
     * Last-clicked chart position; read-only. Same shape as `crosshair`.
     * Written only when `subscribeClick` is true.
     */
    click?: Dict;

    /**
     * Full chart options including defaults; read-only.
     */
    fullChartOptions?: Dict;

    /**
     * Full series options including defaults, keyed by series id; read-only.
     */
    fullSeriesOptions?: Dict;

    /**
     * Full right price scale options including defaults; read-only.
     */
    fullPriceScaleOptions?: Dict;

    /**
     * Full time scale options including defaults; read-only.
     */
    fullTimeScaleOptions?: Dict;

    /**
     * Width of the right price scale in pixels; read-only. Reported on scale
     * resize only when `subscribeSize` is true.
     */
    priceScaleWidth?: number;

    /**
     * Width of the time scale in pixels; read-only. Written only when
     * `subscribeSize` is true.
     */
    timeScaleWidth?: number;

    /**
     * Height of the time scale in pixels; read-only. Written only when
     * `subscribeSize` is true.
     */
    timeScaleHeight?: number;

    /**
     * Visible time range; read-only. Written only when `subscribeVisibleRange`
     * is true.
     */
    visibleRange?: Dict;

    /**
     * Visible logical range in bar indices; read-only. Written only when
     * `subscribeVisibleRange` is true.
     */
    visibleLogicalRange?: Dict;

    /**
     * Dash-assigned callback that fires when a prop changes.
     */
    setProps?: (props: Dict) => void;
};

/**
 * Tradingview Lightweight Chart object
 */
const Tvlwc = ({
    id,
    chartOptions = EMPTY_CHART_OPTIONS,
    series = EMPTY_SERIES,
    subscribeCrosshair = false,
    subscribeClick = false,
    subscribeVisibleRange = false,
    subscribeSize = false,
    reportThrottle = 0,
    width = '100%',
    height = 400,
    setProps,
}: Props) => {
    const containerRef = useRef<HTMLDivElement>(null);
    const chartRef = useRef<IChartApi | null>(null);
    const records = useRef<Map<string, SeriesRecord>>(new Map());
    const chartState = useRef<ChartState>({hasData: false});

    // Dash may hand back a fresh `setProps` on every render. Holding it in a
    // ref keeps it out of effect dependencies, so subscriptions are not torn
    // down and rebuilt on unrelated renders.
    const setPropsRef = useRef(setProps);
    setPropsRef.current = setProps;

    // No epoch counter guards the effects below. React runs a component's
    // effects in declaration order, and StrictMode's development remount tears
    // down and re-runs every effect on the fiber rather than consulting
    // dependency arrays, so the chart is always rebuilt before anything that
    // depends on it re-runs.
    useEffect(() => {
        if (!containerRef.current) {
            return undefined;
        }
        // `autoSize` handles container resizing, replacing the manual window
        // resize listener.
        chartRef.current = createChart(containerRef.current, {
            autoSize: true,
            ...resolveChartOptions(chartOptions),
        });

        return () => {
            chartRef.current?.remove();
            chartRef.current = null;
            records.current.clear();
            chartState.current = {hasData: false};
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useEffect(() => {
        const chart = chartRef.current;
        if (!chart) {
            return;
        }
        chart.applyOptions(resolveChartOptions(chartOptions));
        setPropsRef.current?.({
            fullChartOptions: chart.options(),
            fullTimeScaleOptions: chart.timeScale().options(),
            fullPriceScaleOptions: chart.priceScale('right').options(),
            priceScaleWidth: chart.priceScale('right').width(),
        });
    }, [chartOptions]);

    useEffect(() => {
        const chart = chartRef.current;
        if (!chart) {
            return;
        }
        // `series` is the highest-frequency input prop in a real app, and every
        // read-back is a round trip, so the options dump is written only when
        // reconciliation actually changed a series or its options. A data-only
        // update writes nothing.
        if (!reconcileSeries(chart, chartState.current, records.current, series)) {
            return;
        }
        setPropsRef.current?.({
            fullSeriesOptions: Object.fromEntries(
                Array.from(records.current.entries()).map(([seriesId, record]) => [
                    seriesId,
                    record.api.options(),
                ])
            ),
        });
    }, [series]);

    // Every subscription is paired with its unsubscribe in this effect's
    // cleanup. The v3 component subscribed inside an effect keyed on
    // chartOptions and never unsubscribed, so each options change left three
    // more handlers writing props on every pan frame.
    useEffect(() => {
        const chart = chartRef.current;
        if (!chart) {
            return undefined;
        }
        const timeScale = chart.timeScale();
        const cleanups: (() => void)[] = [];
        const throttle = reportThrottle;

        if (subscribeCrosshair) {
            const emitter = createEmitter(
                (value) => setPropsRef.current?.({crosshair: value as Dict}),
                throttle
            );
            const handler = (param: MouseEventParams<Time>) =>
                emitter.push(buildMouseEvent(param, records.current));
            chart.subscribeCrosshairMove(handler);
            cleanups.push(() => {
                chart.unsubscribeCrosshairMove(handler);
                emitter.cancel();
            });
        }

        if (subscribeClick) {
            const handler = (param: MouseEventParams<Time>) =>
                setPropsRef.current?.({click: buildMouseEvent(param, records.current)});
            chart.subscribeClick(handler);
            cleanups.push(() => chart.unsubscribeClick(handler));
        }

        if (subscribeVisibleRange) {
            const emitter = createEmitter(
                (value) => setPropsRef.current?.(value as Dict),
                throttle
            );
            // Both ranges go in one payload. The library fires the strict-range
            // and logical-range delegates back to back in a single synchronous
            // block, and the emitter coalesces by replacement, so pushing them
            // separately means the second always discards the first.
            const emitRanges = () =>
                emitter.push({
                    visibleRange: timeScale.getVisibleRange(),
                    visibleLogicalRange: timeScale.getVisibleLogicalRange(),
                });
            timeScale.subscribeVisibleTimeRangeChange(emitRanges);
            timeScale.subscribeVisibleLogicalRangeChange(emitRanges);
            cleanups.push(() => {
                timeScale.unsubscribeVisibleTimeRangeChange(emitRanges);
                timeScale.unsubscribeVisibleLogicalRangeChange(emitRanges);
                emitter.cancel();
            });
        }

        if (subscribeSize) {
            // `autoSize` drives this from a ResizeObserver, so dragging a window
            // edge fires it every frame. It is gated and throttled like the
            // other high-frequency reports rather than reported unconditionally.
            const emitter = createEmitter(
                (value) => setPropsRef.current?.(value as Dict),
                throttle
            );
            const onSizeChange = () =>
                emitter.push({
                    timeScaleWidth: timeScale.width(),
                    timeScaleHeight: timeScale.height(),
                    priceScaleWidth: chart.priceScale('right').width(),
                });
            timeScale.subscribeSizeChange(onSizeChange);
            cleanups.push(() => {
                timeScale.unsubscribeSizeChange(onSizeChange);
                emitter.cancel();
            });
        }

        return () => cleanups.forEach((cleanup) => cleanup());
    }, [subscribeCrosshair, subscribeClick, subscribeVisibleRange, subscribeSize, reportThrottle]);

    return <div id={id} ref={containerRef} style={{width, height}} />;
};

export default Tvlwc;
