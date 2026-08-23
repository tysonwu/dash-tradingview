/**
 * The chart component, generic in what sits on the horizontal scale.
 *
 * `Tvlwc`, `Tvlwo` and `Tvlwy` are the same component over `Time`, a price and
 * a maturity in months. That is possible because every API this file touches is
 * already generic upstream: `IChartApi` is defined as `IChartApiBase<Time>`,
 * and `createSeriesMarkers`, `createUpDownMarkers`, `createTextWatermark` and
 * `createImageWatermark` each take the horizontal item as a type parameter. So
 * the chart-specific part of a component is only its constructor and the set of
 * series names it accepts, both of which arrive here as a `ChartKind`.
 *
 * Design rules referenced in the comments below are recorded in
 * `.docs/DESIGN-W3.md`.
 */
import React, {useEffect, useRef, useState} from 'react';
import {
    MismatchDirection,
    createImageWatermark,
    createSeriesMarkers,
    createTextWatermark,
    createUpDownMarkers,
} from 'lightweight-charts';
import type {
    ChartOptionsImpl,
    CreatePriceLineOptions,
    DeepPartial,
    IChartApiBase,
    IPriceLine,
    ISeriesApi,
    ISeriesMarkersPluginApi,
    ISeriesUpDownMarkerPluginApi,
    MouseEventParams,
    SeriesMarker,
    SeriesType,
} from 'lightweight-charts';
import type {
    ChartKind,
    ChartProps,
    Dict,
    PaneSpec,
    SeriesDataItem,
    SeriesSpec,
} from './types';

const FUNCTION_NAMESPACE = 'dashTvlwcFunctions';

const LOCALIZATION_FUNCTION_KEYS = [
    'priceFormatter',
    'tickmarksPriceFormatter',
    'percentageFormatter',
    'tickmarksPercentageFormatter',
    'timeFormatter',
];

const PRICE_FORMAT_FUNCTION_KEYS = ['formatter', 'tickmarksFormatter'];


/**
 * String spellings of the upstream `MismatchDirection` enum, which is numeric
 * and so cannot cross the Dash prop boundary as itself.
 */
const MISMATCH_DIRECTIONS: Record<string, MismatchDirection> = {
    nearestLeft: MismatchDirection.NearestLeft,
    none: MismatchDirection.None,
    nearestRight: MismatchDirection.NearestRight,
};

type WatermarkHandle = {detach: () => void};

type SeriesRecord<THorz, TName extends string> = {
    api: ISeriesApi<SeriesType, THorz>;
    type: TName;
    pane: number;
    spec: Partial<SeriesSpec<THorz, TName>>;
    markersPlugin: ISeriesMarkersPluginApi<THorz> | null;
    upDownPlugin: ISeriesUpDownMarkerPluginApi<THorz> | null;
    priceLines: IPriceLine[];
};

type Records<THorz, TName extends string> = Map<string, SeriesRecord<THorz, TName>>;

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
function resolveFunction(name: unknown, path: string, component: string): unknown {
    if (typeof name !== 'string') {
        return name;
    }
    const namespace = (window as unknown as Dict)[FUNCTION_NAMESPACE] as Dict | undefined;
    const fn = namespace ? namespace[name] : undefined;
    if (typeof fn !== 'function') {
        throw new Error(
            `${component}: ${path} names '${name}', which is not a function on ` +
                `window.${FUNCTION_NAMESPACE}. Register it from an assets JavaScript file.`
        );
    }
    return fn;
}

function resolveKeys(
    source: Dict,
    keys: string[],
    pathPrefix: string,
    component: string
): Dict {
    const out: Dict = {...source};
    for (const key of keys) {
        if (key in out) {
            out[key] = resolveFunction(out[key], `${pathPrefix}.${key}`, component);
        }
    }
    return out;
}

/**
 * Returns a copy of `chartOptions` with named functions resolved. The prop
 * itself is never mutated.
 *
 * Every function-valued option across all three chart types is listed here.
 * A group absent from a given chart's options simply never matches, so one
 * table is cheaper than threading a per-chart one through the component.
 */
function resolveChartOptions<THorz>(
    chartOptions: DeepPartial<ChartOptionsImpl<THorz>>,
    component: string
): DeepPartial<ChartOptionsImpl<THorz>> {
    const source = chartOptions as Dict;
    const out: Dict = {...source};

    if (source.localization) {
        out.localization = resolveKeys(
            source.localization as Dict,
            LOCALIZATION_FUNCTION_KEYS,
            'chartOptions.localization',
            component
        );
    }
    // Time charts only. `HorzScaleOptions` has no `tickMarkFormatter`; the
    // options chart formats its horizontal axis through `localization.precision`
    // and the yield curve chart through `localization.timeFormatter`.
    if (source.timeScale && 'tickMarkFormatter' in (source.timeScale as Dict)) {
        out.timeScale = resolveKeys(
            source.timeScale as Dict,
            ['tickMarkFormatter'],
            'chartOptions.timeScale',
            component
        );
    }
    // `yieldCurve.formatTime` is declared in the upstream typings but never
    // read: the yield curve scale formats through `localization.timeFormatter`,
    // which the group above already covers. Resolving a name here would hand
    // the library a function it ignores and leave the axis on its defaults with
    // nothing to say why, so the key is refused outright.
    if (source.yieldCurve && 'formatTime' in (source.yieldCurve as Dict)) {
        // eslint-disable-next-line no-console
        console.warn(
            `${component}: chartOptions.yieldCurve.formatTime is declared by ` +
                'lightweight-charts but never read by it. Use ' +
                'chartOptions.localization.timeFormatter instead, which ' +
                'receives the same maturity value.'
        );
    }
    return out as DeepPartial<ChartOptionsImpl<THorz>>;
}

function resolveSeriesOptions(
    options: Dict | undefined,
    seriesId: string,
    component: string
): Dict {
    if (!options) {
        return {};
    }
    const out: Dict = {...options};
    if (out.priceFormat && typeof out.priceFormat === 'object') {
        out.priceFormat = resolveKeys(
            out.priceFormat as Dict,
            PRICE_FORMAT_FUNCTION_KEYS,
            `series['${seriesId}'].options.priceFormat`,
            component
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
function applyData<THorz, TName extends string>(
    chart: IChartApiBase<THorz>,
    state: ChartState,
    record: SeriesRecord<THorz, TName>,
    data: SeriesDataItem<THorz>[]
): void {
    const range = state.hasData ? chart.timeScale().getVisibleLogicalRange() : null;
    // The up/down marker plugin has to see the data to know which direction a
    // later update moved in. Its `setData` records the values and then calls the
    // series' own, so routing through it when present is not optional.
    if (record.upDownPlugin) {
        record.upDownPlugin.setData(data as never);
    } else {
        record.api.setData(data as never);
    }
    state.hasData = state.hasData || data.length > 0;
    if (range) {
        chart.timeScale().setVisibleLogicalRange(range);
    }
}

function applyMarkers<THorz, TName extends string>(
    record: SeriesRecord<THorz, TName>,
    markers: SeriesMarker<THorz>[]
): void {
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
function applyPriceLines<THorz, TName extends string>(
    record: SeriesRecord<THorz, TName>,
    priceLines: CreatePriceLineOptions[]
): void {
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

/**
 * Attaches, reconfigures or removes the up/down marker plugin for a series.
 */
const UP_DOWN_TYPES: string[] = ['line', 'area'];

function applyUpDownMarkers<THorz, TName extends string>(
    record: SeriesRecord<THorz, TName>,
    spec: SeriesSpec<THorz, TName>,
    component: string
): void {
    const wanted = spec.upDownMarkers;

    if (!wanted) {
        if (record.upDownPlugin) {
            record.upDownPlugin.detach();
            record.upDownPlugin = null;
        }
        return;
    }
    if (!UP_DOWN_TYPES.includes(spec.type)) {
        // Reachable by changing the type of a series that already had markers,
        // so warn and carry on rather than taking the chart down.
        // eslint-disable-next-line no-console
        console.warn(
            `${component}: series '${spec.id}' sets \`upDownMarkers\` on a ` +
                `'${spec.type}' series. Only ${UP_DOWN_TYPES.join(' and ')} ` +
                'series support them, so they were ignored.'
        );
        return;
    }
    if (record.upDownPlugin) {
        record.upDownPlugin.applyOptions(wanted);
        return;
    }
    record.upDownPlugin = createUpDownMarkers(record.api, wanted);
    // The plugin only learns values through its own setData, so replay what the
    // series already holds rather than waiting for the next data change.
    record.upDownPlugin.setData(record.api.data() as never);
}

function applySpec<THorz, TName extends string>(
    chart: IChartApiBase<THorz>,
    state: ChartState,
    record: SeriesRecord<THorz, TName>,
    spec: SeriesSpec<THorz, TName>,
    component: string
): boolean {
    const previous = record.spec;
    let optionsChanged = false;

    if (!sameValue(previous.options, spec.options)) {
        record.api.applyOptions(resolveSeriesOptions(spec.options, spec.id, component));
        optionsChanged = true;
    }
    if (!sameValue(previous.priceScaleOptions, spec.priceScaleOptions) && spec.priceScaleOptions) {
        record.api.priceScale().applyOptions(spec.priceScaleOptions);
        optionsChanged = true;
    }
    // Before data, so a newly attached plugin is the one that receives it.
    if (!sameValue(previous.upDownMarkers, spec.upDownMarkers)) {
        applyUpDownMarkers(record, spec, component);
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
function reconcileSeries<THorz, TName extends string>(
    chart: IChartApiBase<THorz>,
    state: ChartState,
    records: Records<THorz, TName>,
    series: SeriesSpec<THorz, TName>[],
    kind: ChartKind<THorz>
): boolean {
    const {name: component, definitions} = kind;
    // Validation runs over the whole list before anything is mutated. Failing
    // fast is only useful if the failure is atomic: validating inside the
    // mutation loop would leave earlier series applied, later ones missing, and
    // departed ones still on the chart.
    const seen = new Set<string>();
    for (const spec of series) {
        if (typeof spec.id !== 'string' || spec.id === '') {
            throw new Error(
                `${component}: every entry in \`series\` needs a non-empty string \`id\`.`
            );
        }
        if (seen.has(spec.id)) {
            throw new Error(
                `${component}: duplicate series id '${spec.id}'. ` +
                    'Ids must be unique within `series`.'
            );
        }
        seen.add(spec.id);

        // `hasOwnProperty`, not truthiness: `definitions` is an object
        // literal, so `toString`, `constructor` and `__proto__` would all pass
        // a plain lookup and reach `addSeries`, where the library fails an
        // internal assertion instead of reporting a bad `type`.
        if (!Object.prototype.hasOwnProperty.call(definitions, spec.type)) {
            throw new Error(
                `${component}: series '${spec.id}' has unknown type ` +
                    `'${spec.type}'. Valid types are ` +
                    `${Object.keys(definitions).join(', ')}.`
            );
        }
    }

    let changed = false;

    for (const spec of series) {
        const definition = definitions[spec.type];
        let record = records.get(spec.id);
        // A series API cannot change its own type, so a type change recreates.
        if (record && record.type !== spec.type) {
            // `removeSeries` does not detach series primitives, and the up/down
            // plugin holds a timer that calls back into the model.
            record.upDownPlugin?.detach();
            chart.removeSeries(record.api);
            records.delete(spec.id);
            record = undefined;
            changed = true;
        }
        const pane = spec.pane || 0;
        if (!record) {
            // Options go in at creation rather than through a follow-up
            // applyOptions, so a series carrying `priceScaleId` is never first
            // attached to the default scale and then moved off it. The pane
            // index goes in here too, which is what creates the pane.
            record = {
                api: chart.addSeries(
                    definition,
                    resolveSeriesOptions(spec.options, spec.id, component),
                    pane
                ),
                type: spec.type,
                pane,
                spec: {options: spec.options},
                markersPlugin: null,
                upDownPlugin: null,
                priceLines: [],
            };
            records.set(spec.id, record);
            changed = true;
        } else if (record.pane !== pane) {
            // Moving is not the same as recreating: data, options, markers and
            // price lines all survive the move.
            record.api.moveToPane(pane);
            record.pane = pane;
            changed = true;
        }
        changed = applySpec(chart, state, record, spec, component) || changed;
    }

    for (const [id, record] of Array.from(records.entries())) {
        if (!seen.has(id)) {
            // Removing the series disposes its markers and price lines with it,
            // but not series primitives.
            record.upDownPlugin?.detach();
            chart.removeSeries(record.api);
            records.delete(id);
            changed = true;
        }
    }

    return changed;
}

/**
 * Holds the pane set to what `series[].pane` declares.
 *
 * The library deletes a pane as soon as its last series leaves, whether through
 * `removeSeries` or `moveToPane`, and splices it out of the array so every
 * higher index shifts down. Positional `paneOptions` and the `pane` recorded
 * against each series would both silently start describing the wrong pane.
 *
 * Marking every declared pane as preserved stops the implicit deletion, so
 * indices stay exactly what Python asked for. Panes past the declared maximum
 * are then removed explicitly, which keeps the pane set declarative rather than
 * letting it grow monotonically.
 *
 * Called before reconciliation so the preservation is in place by the time a
 * series is removed or moved.
 */
function preservePanes<THorz>(chart: IChartApiBase<THorz>, highestPane: number): void {
    chart.panes().forEach((pane, index) => {
        pane.setPreserveEmptyPane(index <= highestPane);
    });
}

function trimPanes<THorz>(chart: IChartApiBase<THorz>, highestPane: number): void {
    const panes = chart.panes();
    for (let index = panes.length - 1; index > highestPane; index -= 1) {
        chart.removePane(index);
    }
}

/**
 * Sizes panes positionally. `chart.panes()` is re-read on every call rather than
 * cached: creating a series can create a pane, so a held handle goes stale.
 *
 * `setHeight` works by rewriting the stretch factors of every pane, so mixing it
 * with `stretchFactor` in one spec produces a layout that matches neither. The
 * two are rejected together rather than silently resolved.
 */
/**
 * Pushes a value onto a short history of what has been emitted, used by the echo
 * guard. Bounded because it only has to outlive one round trip through Dash.
 */
const EMIT_HISTORY = 8;

/**
 * Validates a range coming from Python before handing it to the library, which
 * asserts internally and would throw with a message naming neither the prop nor
 * the value.
 *
 * Returns `null` for a range that cannot be applied, rather than throwing: the
 * value is whatever a callback last wrote, so a bad one must not be able to
 * unmount the chart (R4b). The caller skips the write and the chart keeps the
 * viewport it had.
 */
function checkedRange(
    value: Dict,
    prop: string,
    component: string
): {from: unknown; to: unknown} | null {
    const from = value.from;
    const to = value.to;
    if (from === undefined || from === null || to === undefined || to === null) {
        // eslint-disable-next-line no-console
        console.warn(
            `${component}: ${prop} needs both \`from\` and \`to\`, got ` +
                `${JSON.stringify(value)}. Ignored.`
        );
        return null;
    }
    if (typeof from === 'number' && typeof to === 'number' && from > to) {
        // eslint-disable-next-line no-console
        console.warn(
            `${component}: ${prop} has from (${from}) after to (${to}). Ignored.`
        );
        return null;
    }
    return {from, to};
}

/**
 * Which price scale the read-back props describe.
 *
 * Not always the right one. A yield curve chart ships with `leftPriceScale`
 * visible and `rightPriceScale` hidden, and the library sends series to
 * whichever of the two is visible when exactly one is, so reading `'right'`
 * unconditionally would report a zero width for an axis nothing is drawn on.
 * This mirrors the library's own `defaultVisiblePriceScaleId`.
 */
function reportedScaleId<THorz>(chart: IChartApiBase<THorz>): 'left' | 'right' {
    const options = chart.options();
    const left = options.leftPriceScale.visible;
    const right = options.rightPriceScale.visible;
    if (left !== right) {
        return left ? 'left' : 'right';
    }
    return options.defaultVisiblePriceScaleId;
}

function remember(history: unknown[], value: unknown): void {
    history.push(value);
    if (history.length > EMIT_HISTORY) {
        history.shift();
    }
}

function applyPaneOptions<THorz>(
    chart: IChartApiBase<THorz>,
    paneOptions: PaneSpec[],
    component: string
): void {
    if (paneOptions.length === 0) {
        return;
    }
    const panes = chart.panes();
    if (paneOptions.length > panes.length) {
        // Not an error. A callback that moves the last series off a pane
        // removes that pane, and `paneOptions` is usually a constant in the
        // layout rather than something the same callback rewrites, so the
        // sizing outliving the pane is ordinary rather than exceptional.
        // Throwing here unmounts the whole chart for it (R4b).
        // eslint-disable-next-line no-console
        console.warn(
            `${component}: paneOptions has ${paneOptions.length} entries but the chart ` +
                `has ${panes.length} pane(s), so the extra ${paneOptions.length - panes.length} ` +
                'were ignored. Panes are created by `series[].pane`.'
        );
    }
    paneOptions.forEach((options, index) => {
        if (!options || index >= panes.length) {
            return;
        }
        if (typeof options.height === 'number' && typeof options.stretchFactor === 'number') {
            // Same reasoning: warn and leave this pane at whatever size it
            // already has, rather than taking the chart down over one entry.
            // eslint-disable-next-line no-console
            console.warn(
                `${component}: paneOptions[${index}] sets both \`height\` and ` +
                    '`stretchFactor`. Use one or the other; this pane was left ' +
                    'as it was.'
            );
            return;
        }
        const pane = panes[index];
        if (typeof options.height === 'number') {
            pane.setHeight(options.height);
        }
        if (typeof options.stretchFactor === 'number') {
            pane.setStretchFactor(options.stretchFactor);
        }
    });
}

/**
 * Builds the `crosshair` and `click` payloads. `param.seriesData` is keyed by
 * series API object, which means nothing to Python, so it is re-keyed by the
 * user's series id. Only series that actually have data under the cursor are
 * included.
 */
function buildMouseEvent<THorz, TName extends string>(
    param: MouseEventParams<THorz>,
    records: Records<THorz, TName>
): Dict {
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

type CoreProps<THorz, TName extends string> = ChartProps<THorz, TName> & {
    /**
     * Chart options, in whatever shape this chart's constructor accepts. All
     * three extend `ChartOptionsImpl`, which is what the core needs.
     */
    chartOptions: DeepPartial<ChartOptionsImpl<THorz>>;

    /**
     * Which chart to build and which series names to accept.
     */
    kind: ChartKind<THorz>;
};

/**
 * The chart itself.
 *
 * No prop is defaulted here. Defaults belong in the component that wraps this
 * one, because `extract-meta` reads them out of the destructuring pattern of
 * the component it generates Python from, and a default it cannot see becomes
 * a required argument on the Python side (R6).
 */
const ChartCore = <THorz, TName extends string>({
    id,
    chartOptions,
    series,
    paneOptions,
    tick,
    timeScaleAction,
    dataAction,
    crosshairPosition,
    watermark,
    screenshotRequest,
    visibleRange,
    visibleLogicalRange,
    subscribeCrosshair,
    subscribeClick,
    subscribeDblClick,
    subscribeVisibleRange,
    subscribeSize,
    reportThrottle,
    width,
    height,
    setProps,
    kind,
}: CoreProps<THorz, TName>) => {
    // Prefixes every console message, so a warning names the component the user
    // actually wrote rather than the shared core.
    const {name} = kind;

    const containerRef = useRef<HTMLDivElement>(null);
    const chartRef = useRef<IChartApiBase<THorz> | null>(null);
    const records = useRef<Records<THorz, TName>>(new Map());
    const chartState = useRef<ChartState>({hasData: false});

    // R5 echo guard. `visibleRange` and `visibleLogicalRange` are written by the
    // component on pan and read back to drive the chart, so without recording
    // what was last emitted the component's own report arrives as an input and
    // re-applies it.
    // R5 echo guard. Recorded at flush time, where `setProps` actually happens,
    // and kept as a short history rather than one slot: during a continuous pan
    // the chart has already moved on by the time the component's own report
    // completes its round trip through Dash, so testing only the newest value
    // would fail to recognise it and yank the viewport backwards.
    const emittedRanges = useRef<{range: unknown[]; logical: unknown[]}>({
        range: [],
        logical: [],
    });

    // Pane sizing is reapplied only when it actually changes. Users can drag
    // pane separators (`layout.panes.enableResize` defaults to true), and
    // reapplying on every `series` update would snap their drag back.
    const appliedPanes = useRef<{options: PaneSpec[] | null; count: number}>({
        options: null,
        count: 0,
    });

    // Which series `barsInLogicalRange` describes. Map iteration order is
    // creation order, so recreating a series would silently change the answer.
    const firstSeriesId = useRef<string | null>(null);

    // Dash re-dispatches every output prop on every callback response, with a
    // freshly parsed object, so an effect keyed on prop identity alone re-runs
    // whether or not the value changed. Command props therefore compare by
    // value; the `nonce` is what makes a deliberate repeat differ.
    const lastAction = useRef<unknown>(null);
    const lastDataAction = useRef<unknown>(null);

    // Bumped whenever the pane set changes, so the watermark can reattach after
    // `trimPanes` removes the pane it was drawn on.
    const [paneGeneration, setPaneGeneration] = useState(0);

    // The watermark effect keys on a serialised form rather than the prop
    // object. Dash hands back a fresh object on every callback response, and
    // rebuilding an image watermark refetches it and flickers. A guard inside
    // the effect would not do: React runs the cleanup before the body, so an
    // early return would detach the watermark and put nothing back.
    const watermarkKey = watermark ? JSON.stringify(watermark) : '';


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
        const chart = kind.create(containerRef.current, {
            autoSize: true,
            ...resolveChartOptions(chartOptions, name),
        });
        chartRef.current = chart;
        // Seed the pane count from the chart that was just built. Left at zero
        // it never matches, so the first run of the series effect always reads
        // as a pane change, bumps `paneGeneration`, and makes the watermark
        // effect detach and rebuild the watermark it attached moments earlier.
        // For an image watermark that is a second network fetch and a flicker.
        appliedPanes.current = {options: null, count: chart.panes().length};

        return () => {
            // Detach series primitives first: their timers outlive the chart
            // and would call into a destroyed model.
            records.current.forEach((record) => record.upDownPlugin?.detach());
            chartRef.current?.remove();
            chartRef.current = null;
            records.current.clear();
            chartState.current = {hasData: false};
            emittedRanges.current = {range: [], logical: []};
            appliedPanes.current = {options: null, count: 0};
            firstSeriesId.current = null;
            // The command guards go with the chart that ran the command.
            // StrictMode's development remount reuses these refs, so leaving
            // them set makes the throwaway first mount swallow an initial
            // `timeScaleAction` and the real chart never receive it.
            lastAction.current = null;
            lastDataAction.current = null;
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useEffect(() => {
        const chart = chartRef.current;
        if (!chart) {
            return;
        }
        chart.applyOptions(resolveChartOptions(chartOptions, name));
        setPropsRef.current?.({
            fullChartOptions: chart.options(),
            fullTimeScaleOptions: chart.timeScale().options(),
            fullPriceScaleOptions: chart.priceScale(reportedScaleId(chart)).options(),
            priceScaleWidth: chart.priceScale(reportedScaleId(chart)).width(),
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
        const highestPane = series.reduce(
            (highest, spec) => Math.max(highest, spec.pane || 0),
            0
        );
        // Preserve before reconciling: removing or moving a series deletes an
        // emptied pane, and the deletion shifts every higher index down.
        preservePanes(chart, highestPane);
        const changed = reconcileSeries(
            chart,
            chartState.current,
            records.current,
            series,
            kind
        );
        trimPanes(chart, highestPane);

        firstSeriesId.current = series.length > 0 ? series[0].id : null;

        const paneCount = chart.panes().length;
        if (paneCount !== appliedPanes.current.count) {
            // A watermark attached to a pane that has since been trimmed is
            // orphaned rather than detached, so it has to be reattached.
            setPaneGeneration((generation) => generation + 1);
        }
        if (!sameValue(paneOptions, appliedPanes.current.options) ||
            paneCount !== appliedPanes.current.count) {
            applyPaneOptions(chart, paneOptions, name);
            appliedPanes.current = {options: paneOptions, count: paneCount};
        }

        if (!changed) {
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
    }, [series, paneOptions]);

    // Streaming append. `update` places one bar without touching the rest of the
    // series, so unlike `setData` it leaves the visible range alone.
    useEffect(() => {
        const chart = chartRef.current;
        if (!chart || !tick) {
            return;
        }
        const ticks = Array.isArray(tick) ? tick : [tick];
        for (const entry of ticks) {
            const record = records.current.get(entry.id);
            if (!record) {
                // Not an error: a tick can arrive before the callback that
                // creates the series it belongs to.
                // eslint-disable-next-line no-console
                console.warn(
                    `${name}: tick for unknown series id '${entry.id}', ignored.`
                );
                continue;
            }
            try {
                if (record.upDownPlugin) {
                    record.upDownPlugin.update(entry.bar as never,
                                               entry.historicalUpdate);
                } else {
                    record.api.update(entry.bar, entry.historicalUpdate);
                }
                chartState.current.hasData = true;
            } catch (error) {
                // `update` throws on a bar older than the last one, and on
                // `historicalUpdate` for a time that does not exist. Both are
                // reachable from an ordinary callback race, where a slower
                // `series` write lands after a faster tick. Warn and carry on
                // rather than unmounting the chart, and keep the rest of a
                // batch from being lost with it.
                // eslint-disable-next-line no-console
                console.warn(
                    `${name}: tick for series '${entry.id}' was rejected: ` +
                        `${(error as Error).message}`
                );
            }
        }
    }, [tick]);

    // One-off time scale commands.
    useEffect(() => {
        const chart = chartRef.current;
        if (!chart || !timeScaleAction) {
            return;
        }
        // Compare by value, not identity: an unrelated callback that re-emits
        // this prop would otherwise refit the chart and discard the user's pan.
        if (sameValue(timeScaleAction, lastAction.current)) {
            return;
        }
        lastAction.current = timeScaleAction;
        const timeScale = chart.timeScale();
        switch (timeScaleAction.action) {
            case 'fitContent':
                timeScale.fitContent();
                break;
            case 'scrollToRealTime':
                timeScale.scrollToRealTime();
                break;
            case 'resetTimeScale':
                timeScale.resetTimeScale();
                break;
            case 'scrollToPosition':
                timeScale.scrollToPosition(
                    timeScaleAction.position || 0,
                    timeScaleAction.animated !== false
                );
                break;
            default:
                // A typo should not take the chart down with it.
                // eslint-disable-next-line no-console
                console.warn(
                    `${name}: timeScaleAction has unknown action ` +
                        `'${timeScaleAction.action}', ignored.`
                );
        }
    }, [timeScaleAction]);

    // Point-level data queries. Dash cannot call a method and take its return
    // value, so every one of these is a command prop in and a result prop out.
    // All three answers are O(1) in the data, which is what makes them safe to
    // put on the wire at all; anything proportional to the dataset would be a
    // way to ship the data back that Python already has.
    useEffect(() => {
        const chart = chartRef.current;
        if (!chart || !dataAction) {
            return;
        }
        // Same reasoning as `timeScaleAction`: compared by content, so an
        // unrelated callback re-emitting this prop does not pop a second bar.
        if (sameValue(dataAction, lastDataAction.current)) {
            return;
        }
        lastDataAction.current = dataAction;

        const record = records.current.get(dataAction.seriesId);
        if (!record) {
            // Reachable whenever a query races the callback that creates the
            // series, so warn rather than throw.
            // eslint-disable-next-line no-console
            console.warn(
                `${name}: dataAction names unknown series ` +
                    `'${dataAction.seriesId}', ignored.`
            );
            return;
        }
        try {
            switch (dataAction.action) {
                case 'dataByIndex': {
                    const index = dataAction.logicalIndex;
                    if (typeof index !== 'number') {
                        // eslint-disable-next-line no-console
                        console.warn(
                            `${name}: dataAction \`dataByIndex\` needs a ` +
                                'numeric `logicalIndex`, ignored.'
                        );
                        return;
                    }
                    const spelling = dataAction.mismatchDirection || 'none';
                    const direction = MISMATCH_DIRECTIONS[spelling];
                    if (direction === undefined) {
                        // eslint-disable-next-line no-console
                        console.warn(
                            `${name}: dataAction has unknown mismatchDirection ` +
                                `'${spelling}'. Valid values are ` +
                                `${Object.keys(MISMATCH_DIRECTIONS).join(', ')}.`
                        );
                        return;
                    }
                    setPropsRef.current?.({
                        dataResult: {
                            action: 'dataByIndex',
                            seriesId: dataAction.seriesId,
                            logicalIndex: index,
                            data: record.api.dataByIndex(index, direction),
                        },
                    });
                    break;
                }
                case 'lastValue': {
                    setPropsRef.current?.({
                        dataResult: {
                            action: 'lastValue',
                            seriesId: dataAction.seriesId,
                            ...record.api.lastValueData(dataAction.globalLast === true),
                        },
                    });
                    break;
                }
                case 'pop': {
                    const count = dataAction.count === undefined ? 1 : dataAction.count;
                    if (typeof count !== 'number' || count < 1) {
                        // eslint-disable-next-line no-console
                        console.warn(
                            `${name}: dataAction \`pop\` needs a \`count\` ` +
                                'of at least one, ignored.'
                        );
                        return;
                    }
                    const removed = record.api.pop(count);
                    // The up/down plugin caches a value per bar so it can tell
                    // which way a later update moved, and `pop` goes straight to
                    // the series without passing through it, so entries for the
                    // removed bars linger. Replaying `record.api.data()` through
                    // the plugin looks like the fix and is not: `data()` returns
                    // only fulfilled points, so feeding it back deletes every
                    // whitespace point in the series and shifts every logical
                    // index with it. The stale cache is by far the smaller
                    // wrong, and it only shows if a popped bar's time comes back
                    // through `tick`, where it colours the first marker against
                    // the popped value.
                    setPropsRef.current?.({
                        dataResult: {
                            action: 'pop',
                            seriesId: dataAction.seriesId,
                            count,
                            removed,
                        },
                    });
                    break;
                }
                default:
                    // eslint-disable-next-line no-console
                    console.warn(
                        `${name}: dataAction has unknown action ` +
                            `'${dataAction.action}', ignored.`
                    );
            }
        } catch (error) {
            // A query is driven by callback data, so a bad one must not be able
            // to take the chart down with it.
            // eslint-disable-next-line no-console
            console.warn(
                `${name}: dataAction '${dataAction.action}' on ` +
                    `'${dataAction.seriesId}' failed: ${(error as Error).message}`
            );
        }
    }, [dataAction]);

    // Crosshair placed from Python, for cross-chart sync. The library routes
    // this through a synthetic position that deliberately skips the crosshair
    // event, so pointing two charts at each other cannot feed back.
    useEffect(() => {
        const chart = chartRef.current;
        if (!chart) {
            return;
        }
        if (!crosshairPosition) {
            chart.clearCrosshairPosition();
            return;
        }
        const record = records.current.get(crosshairPosition.seriesId);
        if (!record) {
            // Same race as `tick`: the position can arrive before the series.
            // eslint-disable-next-line no-console
            console.warn(
                `${name}: crosshairPosition names unknown series ` +
                    `'${crosshairPosition.seriesId}', ignored.`
            );
            return;
        }
        try {
            chart.setCrosshairPosition(
                crosshairPosition.price,
                crosshairPosition.time as never,
                record.api
            );
        } catch (error) {
            // Throws when the series has no data yet, or the time is outside
            // the scale. Both happen while one chart drives another and the
            // data has not landed, which is the whole point of the prop.
            // eslint-disable-next-line no-console
            console.warn(
                `${name}: could not place the crosshair on ` +
                    `'${crosshairPosition.seriesId}': ${(error as Error).message}`
            );
        }
    }, [crosshairPosition]);

    // Watermark. The handle is a local of this effect run rather than a ref:
    // the cleanup then detaches exactly what this run attached, and cannot be
    // pointed at a handle some other run replaced.
    useEffect(() => {
        const chart = chartRef.current;
        if (!chart || !watermark) {
            return undefined;
        }
        const {pane: paneIndex, imageUrl, ...options} = watermark;
        const pane = chart.panes()[(paneIndex as number) || 0];
        if (!pane) {
            // Reachable whenever a callback removes the series that gave the
            // pane its reason to exist, so warn rather than throw.
            // eslint-disable-next-line no-console
            console.warn(
                `${name}: watermark asks for pane ${paneIndex}, which does not ` +
                    'exist. Panes come from `series[].pane`.'
            );
            return undefined;
        }
        const handle: WatermarkHandle = imageUrl
            ? createImageWatermark(pane, imageUrl as string, options as never)
            : createTextWatermark(pane, options as never);

        // Attaching a pane primitive does not itself invalidate the chart, so
        // the watermark would not appear until something else forced a redraw.
        // A no-op applyOptions is the cheapest way to ask for one.
        chart.applyOptions({});

        return () => {
            // The chart effect is declared first, so on unmount its cleanup has
            // already destroyed this chart. Touching it here would schedule a
            // frame against disposed canvases.
            if (chartRef.current !== chart) {
                return;
            }
            // `detachPrimitive` requests its own update, so no nudge is needed.
            handle.detach();
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [watermarkKey, paneGeneration]);

    // Screenshot, requested by a changing counter and answered on `screenshot`.
    useEffect(() => {
        const chart = chartRef.current;
        if (!chart || !screenshotRequest) {
            return;
        }
        try {
            setPropsRef.current?.({
                screenshot: chart.takeScreenshot().toDataURL('image/png'),
            });
        } catch (error) {
            // A cross-origin image watermark taints the canvas, and toDataURL
            // then refuses to export it. Serve such images with CORS headers.
            // eslint-disable-next-line no-console
            console.warn(
                `${name}: screenshot failed: ${(error as Error).message}`
            );
        }
    }, [screenshotRequest]);

    // Two-way range props. Each skips a value equal to the one it last emitted,
    // so the component's own report does not drive the chart back.
    useEffect(() => {
        const chart = chartRef.current;
        if (!chart || !visibleRange) {
            return;
        }
        if (emittedRanges.current.range.some((seen) => sameValue(visibleRange, seen))) {
            return;
        }
        const range = checkedRange(visibleRange, 'visibleRange', name);
        if (!range) {
            return;
        }
        try {
            chart.timeScale().setVisibleRange(range as never);
        } catch (error) {
            // `setVisibleRange` maps times to bar indices, and the lookup
            // returns null on a chart holding no points at all, which the
            // library turns into an assertion. Two independent callbacks, one
            // writing `series` and one writing this, can land in that order.
            // eslint-disable-next-line no-console
            console.warn(
                `${name}: could not set visibleRange to ` +
                    `${JSON.stringify(visibleRange)}: ${(error as Error).message}`
            );
        }
    }, [visibleRange]);

    useEffect(() => {
        const chart = chartRef.current;
        if (!chart || !visibleLogicalRange) {
            return;
        }
        if (emittedRanges.current.logical.some((seen) =>
            sameValue(visibleLogicalRange, seen))) {
            return;
        }
        const range = checkedRange(visibleLogicalRange, 'visibleLogicalRange', name);
        if (!range) {
            return;
        }
        try {
            chart.timeScale().setVisibleLogicalRange(range as never);
        } catch (error) {
            // eslint-disable-next-line no-console
            console.warn(
                `${name}: could not set visibleLogicalRange to ` +
                    `${JSON.stringify(visibleLogicalRange)}: ` +
                    `${(error as Error).message}`
            );
        }
    }, [visibleLogicalRange]);

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
        const throttle = reportThrottle || 0;

        if (subscribeCrosshair) {
            const emitter = createEmitter(
                (value) => setPropsRef.current?.({crosshair: value as Dict}),
                throttle
            );
            const handler = (param: MouseEventParams<THorz>) =>
                emitter.push(buildMouseEvent(param, records.current));
            chart.subscribeCrosshairMove(handler);
            cleanups.push(() => {
                chart.unsubscribeCrosshairMove(handler);
                emitter.cancel();
            });
        }

        if (subscribeClick) {
            const handler = (param: MouseEventParams<THorz>) =>
                setPropsRef.current?.({click: buildMouseEvent(param, records.current)});
            chart.subscribeClick(handler);
            cleanups.push(() => chart.unsubscribeClick(handler));
        }

        if (subscribeDblClick) {
            const handler = (param: MouseEventParams<THorz>) =>
                setPropsRef.current?.({dblClick: buildMouseEvent(param, records.current)});
            chart.subscribeDblClick(handler);
            cleanups.push(() => chart.unsubscribeDblClick(handler));
        }

        if (subscribeVisibleRange) {
            const emitter = createEmitter((value) => {
                const payload = value as Dict;
                // Record at flush, not at push: only the flushed value reaches
                // Dash, so only that value can come back as an echo.
                remember(emittedRanges.current.range, payload.visibleRange);
                remember(emittedRanges.current.logical, payload.visibleLogicalRange);
                setPropsRef.current?.(payload);
            }, throttle);
            // Both ranges go in one payload. The library fires the strict-range
            // and logical-range delegates back to back in a single synchronous
            // block, and the emitter coalesces by replacement, so pushing them
            // separately means the second always discards the first.
            const emitRanges = () => {
                const range = timeScale.getVisibleRange();
                const logical = timeScale.getVisibleLogicalRange();

                // How much data lies either side of the view. A negative
                // `barsBefore` means the user has scrolled past the start of the
                // data. Reported for the first entry in `series`, by id: map
                // order is creation order, so a recreated series would otherwise
                // silently change which one this describes.
                const seriesId = firstSeriesId.current;
                const record = seriesId ? records.current.get(seriesId) : undefined;
                const bars =
                    record && logical ? record.api.barsInLogicalRange(logical) : null;

                emitter.push({
                    visibleRange: range,
                    visibleLogicalRange: logical,
                    barsInLogicalRange: bars ? {...bars, seriesId} : null,
                });
            };
            timeScale.subscribeVisibleTimeRangeChange(emitRanges);
            timeScale.subscribeVisibleLogicalRangeChange(emitRanges);
            cleanups.push(() => {
                timeScale.unsubscribeVisibleTimeRangeChange(emitRanges);
                timeScale.unsubscribeVisibleLogicalRangeChange(emitRanges);
                emitter.cancel();
                // Nothing is emitted while unsubscribed, so a remembered value
                // would go stale and start suppressing a legitimate write of
                // that same range later on.
                emittedRanges.current = {range: [], logical: []};
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
                    priceScaleWidth: chart.priceScale(reportedScaleId(chart)).width(),
                });
            timeScale.subscribeSizeChange(onSizeChange);
            cleanups.push(() => {
                timeScale.unsubscribeSizeChange(onSizeChange);
                emitter.cancel();
            });
        }

        return () => cleanups.forEach((cleanup) => cleanup());
    }, [
        subscribeCrosshair,
        subscribeClick,
        subscribeDblClick,
        subscribeVisibleRange,
        subscribeSize,
        reportThrottle,
    ]);

    return <div id={id} ref={containerRef} style={{width, height}} />;
};

export default ChartCore;
