/**
 * Prop shapes shared by every chart component.
 *
 * All three chart constructors in lightweight-charts v5 return the same
 * interface parameterised by what sits on the horizontal scale: `IChartApi` is
 * defined as `IChartApiBase<Time>`, and the options and yield curve charts are
 * `IChartApiBase<number>`. The prop surface follows the same shape, so these
 * types take the horizontal item as a parameter and each component instantiates
 * them with its own.
 *
 * `dash-generate-components` resolves imported and generic types, including
 * through an intersection, so a component composing `ChartProps<Time, ...>`
 * with its own additions still generates complete TypedDicts.
 */
import type {
    AreaData,
    BarData,
    BaselineData,
    CandlestickData,
    ChartOptionsImpl,
    CreatePriceLineOptions,
    DeepPartial,
    HistogramData,
    IChartApiBase,
    LineData,
    SeriesDefinition,
    SeriesMarker,
    SeriesType,
    WhitespaceData,
} from 'lightweight-charts';

export type Dict = Record<string, unknown>;

/**
 * A single point on any of the built-in series types. Items carrying only the
 * horizontal position are whitespace.
 */
export type SeriesDataItem<THorz> =
    | AreaData<THorz>
    | BarData<THorz>
    | BaselineData<THorz>
    | CandlestickData<THorz>
    | HistogramData<THorz>
    | LineData<THorz>
    | WhitespaceData<THorz>;

export type SeriesSpec<THorz, TName extends string> = {
    /**
     * Stable identity for this series. Used to key incremental updates and to
     * key the `crosshair`, `click` and `fullSeriesOptions` payloads.
     */
    id: string;

    /**
     * Which kind of series to draw. The names this chart accepts are the ones
     * listed on this field's type; `bar` and `candlestick` need OHLC points,
     * and the rest take a single `value`.
     */
    type: TName;

    /**
     * Data points. Items carrying only `time` are whitespace and render as gaps.
     */
    data: SeriesDataItem<THorz>[];

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
    markers?: SeriesMarker<THorz>[];

    /**
     * Horizontal price lines drawn against this series.
     */
    priceLines?: CreatePriceLineOptions[];

    /**
     * Up and down markers: a temporary marker coloured by whether a revised
     * value rose or fell. Options are `positiveColor`, `negativeColor` and
     * `updateVisibilityDuration`; pass an empty object for the defaults, or
     * omit the key for no markers. Line and area series only.
     *
     * A marker appears only when a `tick` revises a bar the plugin already
     * knows about, and it only learns bars through the series `data`. A tick
     * that appends a new bar therefore draws nothing, and repeated revisions of
     * the same bar are all coloured against the value that arrived in `data`,
     * not against the previous tick.
     */
    upDownMarkers?: Dict;

    /**
     * Index of the pane this series is drawn on, counting from 0. Panes stack
     * vertically and share one horizontal scale. An index one past the last
     * pane creates a pane; further than that is clamped by the library, so keep
     * the indices contiguous. Panes with no series are kept rather than
     * collapsed, so that these indices, and `paneOptions`, stay stable.
     */
    pane?: number;
};

export type PaneSpec = {
    /**
     * Fixed height in pixels. Mutually exclusive with `stretchFactor`, because
     * the library implements a fixed height by rewriting every pane's stretch
     * factor. Ignored when the chart has only one pane.
     */
    height?: number;

    /**
     * Share of the remaining space, relative to the other panes. Proportional
     * sizing survives a resize where a fixed height does not, so prefer it on a
     * responsive page.
     */
    stretchFactor?: number;
};

export type TimeScaleAction = {
    /**
     * One of `fitContent`, `scrollToRealTime`, `resetTimeScale` or
     * `scrollToPosition`.
     */
    action: 'fitContent' | 'scrollToRealTime' | 'resetTimeScale' | 'scrollToPosition';

    /**
     * Bars from the right edge, for `scrollToPosition` only.
     */
    position?: number;

    /**
     * Animate the scroll, for `scrollToPosition` only.
     */
    animated?: boolean;

    /**
     * Change this to repeat an action. These are commands rather than state, and
     * a prop set to the value it already holds produces no change for the
     * component to act on, so repeating `fitContent` needs something to differ.
     */
    nonce?: number;
};

export type DataAction = {
    /**
     * One of `dataByIndex`, `lastValue` or `pop`.
     */
    action: 'dataByIndex' | 'lastValue' | 'pop';

    /**
     * Series to act on, matching an entry in `series`.
     */
    seriesId: string;

    /**
     * Bar index to read, for `dataByIndex` only. Indices are the same ones
     * `visibleLogicalRange` and the mouse payloads report, so zero is the first
     * bar of the series and negative values sit before it.
     */
    logicalIndex?: number;

    /**
     * What to return when no bar sits at `logicalIndex`, for `dataByIndex`
     * only: `none` (the default) answers with `None`, while `nearestLeft` and
     * `nearestRight` answer with the closest bar on that side.
     */
    mismatchDirection?: 'nearestLeft' | 'none' | 'nearestRight';

    /**
     * For `lastValue` only. False, the default, reads the last visible value;
     * true reads the last value in the series whether or not it is on screen.
     */
    globalLast?: boolean;

    /**
     * Bars to remove from the end, for `pop` only. Defaults to one, and is
     * clamped to the length of the series, so asking for more than exists
     * empties it rather than failing.
     */
    count?: number;

    /**
     * Change this to repeat an action, for the same reason `timeScaleAction`
     * carries one: a prop reset to the value it already holds is not a change.
     */
    nonce?: number;
};

export type CrosshairPosition<THorz> = {
    /**
     * Series whose price scale the `price` is read against.
     */
    seriesId: string;

    /**
     * Vertical position, as a price.
     */
    price: number;

    /**
     * Horizontal position, in the same form the series data uses.
     */
    time: THorz;
};

export type WatermarkSpec = {
    /**
     * Pane to draw on. Defaults to the first.
     */
    pane?: number;

    /**
     * Image source. Given this, an image watermark is drawn and `lines` is
     * ignored; otherwise a text watermark is drawn.
     */
    imageUrl?: string;

    /**
     * Text lines, each with `text` and optionally `color`, `fontSize`,
     * `fontFamily`, `fontStyle`, `lineHeight`.
     */
    lines?: Dict[];

    /**
     * Remaining options are passed through: `horzAlign` and `vertAlign` for
     * text, `maxWidth`, `maxHeight`, `padding` and `alpha` for images.
     */
    [key: string]: unknown;
};

export type Tick<THorz> = {
    /**
     * Id of the series to append to, matching an entry in `series`.
     */
    id: string;

    /**
     * The bar to append. Appends when its horizontal position is after the last
     * bar, replaces when the position matches.
     */
    bar: SeriesDataItem<THorz>;

    /**
     * Amend a bar that is not the last one. Slower than a plain append, and it
     * cannot insert a bar that does not already exist: naming a position with
     * no bar is rejected with a console warning. To add missing history,
     * rebuild `series[].data` instead.
     */
    historicalUpdate?: boolean;
};

/**
 * Every prop shared by the chart components. A component composes this with the
 * `chartOptions` type its own constructor accepts.
 */
export type ChartProps<THorz, TName extends string> = {
    /**
     * The ID of this component.
     */
    id?: string;

    /**
     * The series drawn on this chart, each carrying its own id, type, data,
     * options, markers and price lines.
     */
    series: SeriesSpec<THorz, TName>[];

    /**
     * Pane sizing, positional by pane index. Panes come into existence through
     * `series[].pane`; this only sizes them.
     */
    paneOptions: PaneSpec[];

    /**
     * Appends a bar to a series without replacing its data, which is what keeps
     * the visible range steady while streaming. Accepts one tick or a list, so
     * a batch of bars costs one prop write.
     *
     * Because this is a prop rather than an event, a tick identical to the
     * previous one does not re-fire. A tick naming an unknown series id is
     * ignored with a console warning, since it can arrive before the callback
     * that creates the series.
     */
    tick?: Tick<THorz> | Tick<THorz>[] | null;

    /**
     * Runs a one-off horizontal scale command: `fitContent`,
     * `scrollToRealTime`, `resetTimeScale` or `scrollToPosition`. The value is
     * compared by content, so re-emitting the same command from an unrelated
     * callback does nothing; change the `nonce` to ask for a genuine repeat.
     */
    timeScaleAction?: TimeScaleAction | null;

    /**
     * Asks a series about its own data, answering on `dataResult`.
     *
     * `dataByIndex` reads back the single bar at `logicalIndex`, `lastValue`
     * reads back the last price and the colour it is drawn in, and `pop`
     * removes bars from the end and reads back what it removed. All three are
     * O(1) in what crosses the wire, so none of them ships the dataset back.
     *
     * `pop` leaves the chart holding less than `series[].data` describes, in
     * the same way `tick` leaves it holding more. Both are deliberate: the next
     * callback that writes `series` restores the prop as the whole truth.
     *
     * Two things to know about `pop` specifically. It is the only action here
     * that destroys anything, so a component that unmounts and remounts while
     * this prop still holds a `pop` runs it again against the new chart; put
     * the chart inside `dcc.Tabs` and it will pop once per visit. And on a
     * series with `upDownMarkers`, the plugin keeps caching the popped bars, so
     * a later `tick` at one of those times draws its first marker against the
     * popped value.
     *
     * Compared by content, like `timeScaleAction`, so change the `nonce` to
     * repeat a query.
     */
    dataAction?: DataAction | null;

    /**
     * Places the crosshair without a pointer, for syncing one chart to another.
     * `None` clears it. Positioning this way deliberately does not emit a
     * `crosshair` report, so two charts pointed at each other cannot loop.
     */
    crosshairPosition?: CrosshairPosition<THorz> | null;

    /**
     * Draws a watermark over a pane. Give `imageUrl` for an image, or `lines`
     * for text. `None` removes it.
     */
    watermark?: WatermarkSpec | null;

    /**
     * Increment to capture the chart; the PNG arrives as a data URI on the
     * `screenshot` prop. An integer counter such as a button's `n_clicks` is
     * the intended shape, and `0` means no request.
     *
     * The capture excludes the crosshair. An image watermark loaded from
     * another origin taints the canvas and makes the export fail, so serve one
     * with CORS headers if screenshots matter.
     */
    screenshotRequest?: number;

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
     * Whether to report double clicks through the `dblClick` prop.
     */
    subscribeDblClick?: boolean;

    /**
     * Whether to report scale range changes through `visibleRange` and
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
     * Last double-clicked chart position; read-only. Same shape as `crosshair`.
     * Written only when `subscribeDblClick` is true.
     */
    dblClick?: Dict;

    /**
     * The most recent screenshot as a PNG data URI; read-only. Written once per
     * change of `screenshotRequest`.
     */
    screenshot?: string;

    /**
     * Answer to the last `dataAction`; read-only. Always carries the `action`
     * and `seriesId` it answers, so a callback fed by several queries can tell
     * which one arrived, plus:
     *
     * - `dataByIndex`: `logicalIndex`, and `data` holding the whole data point
     *   or `None` when the index falls outside the series.
     * - `lastValue`: `noData`, and when that is false, `price` and `color`.
     * - `pop`: `count` as asked for, and `removed` holding the bars that were
     *   actually taken off, newest first. It is shorter than `count` when the
     *   series held fewer bars than that.
     *
     * An action naming an unknown series, or one the library rejects, writes
     * nothing and warns on the console instead, so a stale answer can outlive
     * the request that failed. The `action` and `seriesId` are what tell the
     * two apart.
     */
    dataResult?: Dict;

    /**
     * Bars available around the visible range, as `{barsBefore, barsAfter,
     * from, to, seriesId}`; read-only. Describes the first entry in `series`,
     * and names it in `seriesId`. A negative `barsBefore` means the user has
     * scrolled past the start of the data, which is the signal to fetch more
     * history. Written only when `subscribeVisibleRange` is true.
     */
    barsInLogicalRange?: Dict;

    /**
     * Full chart options including defaults; read-only.
     */
    fullChartOptions?: Dict;

    /**
     * Full series options including defaults, keyed by series id; read-only.
     */
    fullSeriesOptions?: Dict;

    /**
     * Full options of the chart's default visible price scale, including
     * defaults; read-only. That is the right scale on most charts, but the left
     * one wherever only the left is visible, which is how a yield curve chart
     * ships.
     */
    fullPriceScaleOptions?: Dict;

    /**
     * Full horizontal scale options including defaults; read-only.
     */
    fullTimeScaleOptions?: Dict;

    /**
     * Width in pixels of the chart's default visible price scale; read-only.
     * Picked the same way as `fullPriceScaleOptions`. Reported on scale resize
     * only when `subscribeSize` is true.
     */
    priceScaleWidth?: number;

    /**
     * Width of the horizontal scale in pixels; read-only. Written only when
     * `subscribeSize` is true.
     */
    timeScaleWidth?: number;

    /**
     * Height of the horizontal scale in pixels; read-only. Written only when
     * `subscribeSize` is true.
     */
    timeScaleHeight?: number;

    /**
     * Visible range, as `{from, to}` in the same form the series data uses.
     * Two-way: set it to move the chart, and read it to follow the user, though
     * it is only reported while `subscribeVisibleRange` is true. The library
     * clamps a requested range to the data that exists, so what is reported
     * back will often not equal what was set.
     */
    visibleRange?: Dict;

    /**
     * Visible range in bar indices, as `{from, to}`. Two-way, like
     * `visibleRange`, and reported only while `subscribeVisibleRange` is true.
     * Indices may be fractional, and may fall outside the data. Setting both
     * this and `visibleRange` in one callback is ambiguous; this one wins.
     */
    visibleLogicalRange?: Dict;

    /**
     * Dash-assigned callback that fires when a prop changes.
     */
    setProps?: (props: Dict) => void;
};

/**
 * What one chart component contributes beyond the shared props: which
 * constructor to call, which series names it accepts, and what to call itself
 * in a console warning.
 */
export type ChartKind<THorz> = {
    /**
     * Component name, used only to prefix console messages.
     */
    name: string;

    /**
     * The upstream constructor. `createChart`, `createOptionsChart` and
     * `createYieldCurveChart` all return `IChartApiBase` parameterised by what
     * sits on the horizontal scale, so the core needs nothing else from them.
     */
    create: (
        container: HTMLElement,
        options: DeepPartial<ChartOptionsImpl<THorz>>
    ) => IChartApiBase<THorz>;

    /**
     * Series names this chart accepts, mapped to the upstream definitions that
     * `addSeries` expects. A name outside this map is rejected by name, so the
     * error says which names are valid for this component.
     */
    definitions: Record<string, SeriesDefinition<SeriesType>>;
};
