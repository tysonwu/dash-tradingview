# AUTO GENERATED FILE - DO NOT EDIT

export tvlwo

"""
    tvlwo(;kwargs...)

A Tvlwo component.
Tradingview Lightweight Chart on a price axis, for option payoff and
volatility curves. Points carry `time` as a number, which the chart reads as
a position on the horizontal price scale rather than as a moment, so a strike
of 105.5 is written `{'time': 105.5, 'value': ...}`. Points must still be
unique and ascending in `time`.
Keyword arguments:
- `id` (String; optional): The ID of this component.
- `barsInLogicalRange` (Bool | Real | String | Dict | Array; optional): Bars available around the visible range, as `{barsBefore, barsAfter,
from, to, seriesId}`; read-only. Describes the first entry in `series`,
and names it in `seriesId`. A negative `barsBefore` means the user has
scrolled past the start of the data, which is the signal to fetch more
history. Written only when `subscribeVisibleRange` is true.
- `chartOptions` (optional): Object containing all chart options. Mirrors the `PriceChartOptions`
interface of the underlying charting library, which is the ordinary chart
options object with one addition: `localization.precision` sets how many
decimal places the horizontal axis labels carry.

There is no `timeScale.tickMarkFormatter` here. That option belongs to
time charts; the horizontal axis is formatted through
`localization.precision` instead. Every other `timeScale` option applies
unchanged, including `barSpacing`, `minBarSpacing`, the borders and the
conflation group.

Option values that must be functions, such as
`localization.priceFormatter`, are given as the string name of a function
registered on `window.dashTvlwcFunctions`.. chartOptions has the following type: lists containing elements 'localization', 'width', 'height', 'autoSize', 'layout', 'leftPriceScale', 'rightPriceScale', 'defaultVisiblePriceScaleId', 'overlayPriceScales', 'timeScale', 'crosshair', 'grid', 'handleScroll', 'handleScale', 'kineticScroll', 'trackingMode', 'addDefaultPane', 'hoveredSeriesOnTop'.
Those elements have the following types:
  - `localization` (Bool | Real | String | Dict | Array; optional): Localization options for formatting price values and other chart elements.
  - `width` (Real; optional): Width of the chart in pixels
@,defaultValue,If `0` (default) or none value provided, then a size of the widget will be calculated based its container's size.
  - `height` (Real; optional): Height of the chart in pixels
@,defaultValue,If `0` (default) or none value provided, then a size of the widget will be calculated based its container's size.
  - `autoSize` (Bool; optional): Setting this flag to `true` will make the chart watch the chart container's size and automatically resize the chart to fit its container whenever the size changes.

This feature requires [`ResizeObserver`](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver) class to be available in the global scope.
Note that calling code is responsible for providing a polyfill if required. If the global scope does not have `ResizeObserver`, a warning will appear and the flag will be ignored.

Please pay attention that `autoSize` option and explicit sizes options `width` and `height` don't conflict with one another.
If you specify `autoSize` flag, then `width` and `height` options will be ignored unless `ResizeObserver` has failed. If it fails then the values will be used as fallback.

The flag `autoSize` could also be set with and unset with `applyOptions` function.
```js
const chart = LightweightCharts.createChart(document.body, {
    autoSize: true,
});
```
  - `layout` (Bool | Real | String | Dict | Array; optional): Layout options
  - `leftPriceScale` (Bool | Real | String | Dict | Array; optional): Left price scale options
  - `rightPriceScale` (Bool | Real | String | Dict | Array; optional): Right price scale options
  - `defaultVisiblePriceScaleId` (a value equal to: None, 'left', 'right'; optional): The price scale to prefer when the chart needs a default side and both left and right price scales
share the same visibility state (both visible or both hidden).
This affects behaviors that depend on the pane's default side, such as:
- horizontal grid lines
- overlay series label placement
- the price scale used when adding a series without an explicit `priceScaleId`
- crosshair price coordinate conversion and magnet snapping
@,defaultValue,`'right'`
  - `overlayPriceScales` (Bool | Real | String | Dict | Array; optional): Overlay price scale options
  - `timeScale` (Bool | Real | String | Dict | Array; optional): Time scale options
  - `crosshair` (Bool | Real | String | Dict | Array; optional): The crosshair shows the intersection of the price and time scale values at any point on the chart.
  - `grid` (Bool | Real | String | Dict | Array; optional): A grid is represented in the chart background as a vertical and horizontal lines drawn at the levels of visible marks of price and the time scales.
  - `handleScroll` (Bool; optional): Scroll options, or a boolean flag that enables/disables scrolling
  - `handleScale` (Bool; optional): Scale options, or a boolean flag that enables/disables scaling
  - `kineticScroll` (Bool | Real | String | Dict | Array; optional): Kinetic scroll options
  - `trackingMode` (Bool | Real | String | Dict | Array; optional): TrackingModeOptions
@,inheritDoc,TrackingModeOptions
  - `addDefaultPane` (Bool; optional): Whether to add a default pane to the chart
Disable this option when you want to create a chart with no panes and add them manually
@,defaultValue,`true`
  - `hoveredSeriesOnTop` (Bool; optional): Whether to draw the currently hovered series above the other series in the same pane.

This only affects drawing and hit-testing order while the series is hovered; it doesn't
change the stored series order.
@,defaultValue,`true`
- `click` (Bool | Real | String | Dict | Array; optional): Last-clicked chart position; read-only. Same shape as `crosshair`.
Written only when `subscribeClick` is true.
- `crosshair` (Bool | Real | String | Dict | Array; optional): Crosshair position; read-only. Carries `time`, `logical`, `paneIndex`,
`point`, `seriesData` and `price` keyed by series id, `hoveredSeriesId`
and `hoveredObjectId`. `seriesData` holds whole data points and is
present only for series with data under the cursor; `price` is the price
at the cursor on each series' own scale and is defined between bars too.
Written only when `subscribeCrosshair` is true.
- `crosshairPosition` (Bool | Real | String | Dict | Array; optional): Places the crosshair without a pointer, for syncing one chart to another.
`None` clears it. Positioning this way deliberately does not emit a
`crosshair` report, so two charts pointed at each other cannot loop.
- `dataAction` (Bool | Real | String | Dict | Array; optional): Asks a series about its own data, answering on `dataResult`.

`dataByIndex` reads back the single bar at `logicalIndex`, `lastValue`
reads back the last price and the colour it is drawn in, and `pop`
removes bars from the end and reads back what it removed. All three are
O(1) in what crosses the wire, so none of them ships the dataset back.

`pop` leaves the chart holding less than `series[].data` describes, in
the same way `tick` leaves it holding more. Both are deliberate: the next
callback that writes `series` restores the prop as the whole truth.

Two things to know about `pop` specifically. It is the only action here
that destroys anything, so a component that unmounts and remounts while
this prop still holds a `pop` runs it again against the new chart; put
the chart inside `dcc.Tabs` and it will pop once per visit. And on a
series with `upDownMarkers`, the plugin keeps caching the popped bars, so
a later `tick` at one of those times draws its first marker against the
popped value.

Compared by content, like `timeScaleAction`, so change the `nonce` to
repeat a query.
- `dataResult` (Bool | Real | String | Dict | Array; optional): Answer to the last `dataAction`; read-only. Always carries the `action`
and `seriesId` it answers, so a callback fed by several queries can tell
which one arrived, plus:

- `dataByIndex`: `logicalIndex`, and `data` holding the whole data point
  or `None` when the index falls outside the series.
- `lastValue`: `noData`, and when that is false, `price` and `color`.
- `pop`: `count` as asked for, and `removed` holding the bars that were
  actually taken off, newest first. It is shorter than `count` when the
  series held fewer bars than that.

An action naming an unknown series, or one the library rejects, writes
nothing and warns on the console instead, so a stale answer can outlive
the request that failed. The `action` and `seriesId` are what tell the
two apart.
- `dblClick` (Bool | Real | String | Dict | Array; optional): Last double-clicked chart position; read-only. Same shape as `crosshair`.
Written only when `subscribeDblClick` is true.
- `fullChartOptions` (Bool | Real | String | Dict | Array; optional): Full chart options including defaults; read-only.
- `fullPriceScaleOptions` (Bool | Real | String | Dict | Array; optional): Full options of the chart's default visible price scale, including
defaults; read-only. That is the right scale on most charts, but the left
one wherever only the left is visible, which is how a yield curve chart
ships.
- `fullSeriesOptions` (Bool | Real | String | Dict | Array; optional): Full series options including defaults, keyed by series id; read-only.
- `fullTimeScaleOptions` (Bool | Real | String | Dict | Array; optional): Full horizontal scale options including defaults; read-only.
- `height` (String | Real; optional): Sets height of the parent div of the chart.
- `paneOptions` (optional): Pane sizing, positional by pane index. Panes come into existence through
`series[].pane`; this only sizes them.. paneOptions has the following type: Array of lists containing elements 'height', 'stretchFactor'.
Those elements have the following types:
  - `height` (Real; optional): Fixed height in pixels. Mutually exclusive with `stretchFactor`, because
the library implements a fixed height by rewriting every pane's stretch
factor. Ignored when the chart has only one pane.
  - `stretchFactor` (Real; optional): Share of the remaining space, relative to the other panes. Proportional
sizing survives a resize where a fixed height does not, so prefer it on a
responsive page.s
- `priceScaleWidth` (Real; optional): Width in pixels of the chart's default visible price scale; read-only.
Picked the same way as `fullPriceScaleOptions`. Reported on scale resize
only when `subscribeSize` is true.
- `reportThrottle` (Real; optional): Milliseconds to coalesce reports over, applied to every `subscribe*`
stream. Zero batches to one report per animation frame.
- `screenshot` (String; optional): The most recent screenshot as a PNG data URI; read-only. Written once per
change of `screenshotRequest`.
- `screenshotRequest` (Real; optional): Increment to capture the chart; the PNG arrives as a data URI on the
`screenshot` prop. An integer counter such as a button's `n_clicks` is
the intended shape, and `0` means no request.

The capture excludes the crosshair. An image watermark loaded from
another origin taints the canvas and makes the export fail, so serve one
with CORS headers if screenshots matter.
- `series` (optional): The series drawn on this chart, each carrying its own id, type, data,
options, markers and price lines.. series has the following type: Array of lists containing elements 'id', 'type', 'data', 'options', 'priceScaleOptions', 'markers', 'priceLines', 'upDownMarkers', 'pane'.
Those elements have the following types:
  - `id` (String; required): Stable identity for this series. Used to key incremental updates and to
key the `crosshair`, `click` and `fullSeriesOptions` payloads.
  - `type` (a value equal to: 'area', 'bar', 'baseline', 'candlestick', 'histogram', 'line'; required): Which kind of series to draw. The names this chart accepts are the ones
listed on this field's type; `bar` and `candlestick` need OHLC points,
and the rest take a single `value`.
  - `data` (Array of Bool | Real | String | Dict | Arrays; required): Data points. Items carrying only `time` are whitespace and render as gaps.
  - `options` (Bool | Real | String | Dict | Array; optional): Series options. See the `SeriesOptionsCommon` interface of the underlying
charting library, plus the options specific to this series type.
  - `priceScaleOptions` (Bool | Real | String | Dict | Array; optional): Options for the price scale this series is attached to. This is where
`scaleMargins` lives; it is not a series option.
  - `markers` (Bool | Real | String | Dict | Array; optional): Markers drawn against this series.
  - `priceLines` (Bool | Real | String | Dict | Array; optional): Horizontal price lines drawn against this series.
  - `upDownMarkers` (Bool | Real | String | Dict | Array; optional): Up and down markers: a temporary marker coloured by whether a revised
value rose or fell. Options are `positiveColor`, `negativeColor` and
`updateVisibilityDuration`; pass an empty object for the defaults, or
omit the key for no markers. Line and area series only.

A marker appears only when a `tick` revises a bar the plugin already
knows about, and it only learns bars through the series `data`. A tick
that appends a new bar therefore draws nothing, and repeated revisions of
the same bar are all coloured against the value that arrived in `data`,
not against the previous tick.
  - `pane` (Real; optional): Index of the pane this series is drawn on, counting from 0. Panes stack
vertically and share one horizontal scale. An index one past the last
pane creates a pane; further than that is clamped by the library, so keep
the indices contiguous. Panes with no series are kept rather than
collapsed, so that these indices, and `paneOptions`, stay stable.s
- `setProps` (optional): Dash-assigned callback that fires when a prop changes.
- `subscribeClick` (Bool; optional): Whether to report chart clicks through the `click` prop.
- `subscribeCrosshair` (Bool; optional): Whether to report crosshair movement through the `crosshair` prop. Off by
default: every report is a network round trip, and crosshair movement
fires on every mouse move.
- `subscribeDblClick` (Bool; optional): Whether to report double clicks through the `dblClick` prop.
- `subscribeSize` (Bool; optional): Whether to report scale dimensions through `timeScaleWidth`,
`timeScaleHeight` and `priceScaleWidth`. Off by default: `autoSize`
drives these from a resize observer, so they fire every frame while the
window is being dragged.
- `subscribeVisibleRange` (Bool; optional): Whether to report scale range changes through `visibleRange` and
`visibleLogicalRange`. Off by default: these fire continuously while
panning and zooming.
- `tick` (Bool | Real | String | Dict | Array; optional): Appends a bar to a series without replacing its data, which is what keeps
the visible range steady while streaming. Accepts one tick or a list, so
a batch of bars costs one prop write.

Because this is a prop rather than an event, a tick identical to the
previous one does not re-fire. A tick naming an unknown series id is
ignored with a console warning, since it can arrive before the callback
that creates the series.
- `timeScaleAction` (Bool | Real | String | Dict | Array; optional): Runs a one-off horizontal scale command: `fitContent`,
`scrollToRealTime`, `resetTimeScale` or `scrollToPosition`. The value is
compared by content, so re-emitting the same command from an unrelated
callback does nothing; change the `nonce` to ask for a genuine repeat.
- `timeScaleHeight` (Real; optional): Height of the horizontal scale in pixels; read-only. Written only when
`subscribeSize` is true.
- `timeScaleWidth` (Real; optional): Width of the horizontal scale in pixels; read-only. Written only when
`subscribeSize` is true.
- `visibleLogicalRange` (Bool | Real | String | Dict | Array; optional): Visible range in bar indices, as `{from, to}`. Two-way, like
`visibleRange`, and reported only while `subscribeVisibleRange` is true.
Indices may be fractional, and may fall outside the data. Setting both
this and `visibleRange` in one callback is ambiguous; this one wins.
- `visibleRange` (Bool | Real | String | Dict | Array; optional): Visible range, as `{from, to}` in the same form the series data uses.
Two-way: set it to move the chart, and read it to follow the user, though
it is only reported while `subscribeVisibleRange` is true. The library
clamps a requested range to the data that exists, so what is reported
back will often not equal what was set.
- `watermark` (Bool | Real | String | Dict | Array; optional): Draws a watermark over a pane. Give `imageUrl` for an image, or `lines`
for text. `None` removes it.
- `width` (String | Real; optional): Sets width of the parent div of the chart.
"""
function tvlwo(; kwargs...)
        available_props = Symbol[:id, :barsInLogicalRange, :chartOptions, :click, :crosshair, :crosshairPosition, :dataAction, :dataResult, :dblClick, :fullChartOptions, :fullPriceScaleOptions, :fullSeriesOptions, :fullTimeScaleOptions, :height, :paneOptions, :priceScaleWidth, :reportThrottle, :screenshot, :screenshotRequest, :series, :subscribeClick, :subscribeCrosshair, :subscribeDblClick, :subscribeSize, :subscribeVisibleRange, :tick, :timeScaleAction, :timeScaleHeight, :timeScaleWidth, :visibleLogicalRange, :visibleRange, :watermark, :width]
        wild_props = Symbol[]
        return Component("tvlwo", "Tvlwo", "dash_tvlwc", available_props, wild_props; kwargs...)
end

