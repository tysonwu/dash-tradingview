% Auto-generated: do not edit by hand
\name{tvlwy}

\alias{tvlwy}

\title{Tvlwy component}

\description{
Tradingview Lightweight Chart on a maturity axis, for yield curves. Points carry `time` as a number of `chartOptions.yieldCurve.baseResolution` units from `startTimeRange`, which defaults to months from zero, so a ten-year point is written `{'time': 120, 'value': 4.3}`. The chart spaces maturities by that value rather than evenly, which is what makes the short end of a curve read correctly. Points must be unique and ascending in `time`.
}

\usage{
tvlwy(id=NULL, barsInLogicalRange=NULL, chartOptions=NULL,
click=NULL, crosshair=NULL, crosshairPosition=NULL,
dataAction=NULL, dataResult=NULL, dblClick=NULL,
fullChartOptions=NULL, fullPriceScaleOptions=NULL,
fullSeriesOptions=NULL, fullTimeScaleOptions=NULL,
height=NULL, paneOptions=NULL, priceScaleWidth=NULL,
reportThrottle=NULL, screenshot=NULL,
screenshotRequest=NULL, series=NULL, subscribeClick=NULL,
subscribeCrosshair=NULL, subscribeDblClick=NULL,
subscribeSize=NULL, subscribeVisibleRange=NULL, tick=NULL,
timeScaleAction=NULL, timeScaleHeight=NULL,
timeScaleWidth=NULL, visibleLogicalRange=NULL,
visibleRange=NULL, watermark=NULL, width=NULL)
}

\arguments{
\item{id}{Character. The ID of this component.}

\item{barsInLogicalRange}{Logical | numeric | character | named list | unnamed list. Bars available around the visible range, as `{barsBefore, barsAfter,
from, to, seriesId}`; read-only. Describes the first entry in `series`,
and names it in `seriesId`. A negative `barsBefore` means the user has
scrolled past the start of the data, which is the signal to fetch more
history. Written only when `subscribeVisibleRange` is true.}

\item{chartOptions}{Lists containing elements 'yieldcurve', 'localization', 'width', 'height', 'autosize', 'layout', 'leftpricescale', 'rightpricescale', 'defaultvisiblepricescaleid', 'overlaypricescales', 'timescale', 'crosshair', 'grid', 'handlescroll', 'handlescale', 'kineticscroll', 'trackingmode', 'adddefaultpane', 'hoveredseriesontop'.
those elements have the following types:
  - yieldcurve (logical | numeric | character | named list | unnamed list; optional): yield curve specific options.
this object contains all the settings related to how the yield curve is displayed and behaves.
  - localization (logical | numeric | character | named list | unnamed list; optional): localization options.
  - width (numeric; optional): width of the chart in pixels
@,defaultvalue,if `0` (default) or none value provided, then a size of the widget will be calculated based its container's size.
  - height (numeric; optional): height of the chart in pixels
@,defaultvalue,if `0` (default) or none value provided, then a size of the widget will be calculated based its container's size.
  - autosize (logical; optional): setting this flag to `true` will make the chart watch the chart container's size and automatically resize the chart to fit its container whenever the size changes.

this feature requires [`resizeobserver`](https://developer.mozilla.org/en-us/docs/web/api/resizeobserver) class to be available in the global scope.
note that calling code is responsible for providing a polyfill if required. if the global scope does not have `resizeobserver`, a warning will appear and the flag will be ignored.

please pay attention that `autosize` option and explicit sizes options `width` and `height` don't conflict with one another.
if you specify `autosize` flag, then `width` and `height` options will be ignored unless `resizeobserver` has failed. if it fails then the values will be used as fallback.

the flag `autosize` could also be set with and unset with `applyoptions` function.
```js
const chart = lightweightcharts.createchart(document.body, {
    autosize: true,
});
```
  - layout (logical | numeric | character | named list | unnamed list; optional): layout options
  - leftpricescale (logical | numeric | character | named list | unnamed list; optional): left price scale options
  - rightpricescale (logical | numeric | character | named list | unnamed list; optional): right price scale options
  - defaultvisiblepricescaleid (a value equal to: none, 'left', 'right'; optional): the price scale to prefer when the chart needs a default side and both left and right price scales
share the same visibility state (both visible or both hidden).
this affects behaviors that depend on the pane's default side, such as:
- horizontal grid lines
- overlay series label placement
- the price scale used when adding a series without an explicit `pricescaleid`
- crosshair price coordinate conversion and magnet snapping
@,defaultvalue,`'right'`
  - overlaypricescales (logical | numeric | character | named list | unnamed list; optional): overlay price scale options
  - timescale (logical | numeric | character | named list | unnamed list; optional): time scale options
  - crosshair (logical | numeric | character | named list | unnamed list; optional): the crosshair shows the intersection of the price and time scale values at any point on the chart.
  - grid (logical | numeric | character | named list | unnamed list; optional): a grid is represented in the chart background as a vertical and horizontal lines drawn at the levels of visible marks of price and the time scales.
  - handlescroll (logical; optional): scroll options, or a boolean flag that enables/disables scrolling
  - handlescale (logical; optional): scale options, or a boolean flag that enables/disables scaling
  - kineticscroll (logical | numeric | character | named list | unnamed list; optional): kinetic scroll options
  - trackingmode (logical | numeric | character | named list | unnamed list; optional): trackingmodeoptions
@,inheritdoc,trackingmodeoptions
  - adddefaultpane (logical; optional): whether to add a default pane to the chart
disable this option when you want to create a chart with no panes and add them manually
@,defaultvalue,`true`
  - hoveredseriesontop (logical; optional): whether to draw the currently hovered series above the other series in the same pane.

this only affects drawing and hit-testing order while the series is hovered; it doesn't
change the stored series order.
@,defaultvalue,`true`. Object containing all chart options. Mirrors the `YieldCurveChartOptions`
interface of the underlying charting library: the ordinary chart options
object plus a `yieldCurve` group of `baseResolution` (the smallest time
unit, default 1 month), `minimumTimeRange` (default 120, so ten years are
always in view) and `startTimeRange` (default 0).

To label the maturity axis, give `localization.timeFormatter` the string
name of a function registered on `window.dashTvlwcFunctions`. It receives
the maturity in `baseResolution` units and returns the label; without one
the axis falls back to `6M` and `5Y` style defaults.

`yieldCurve.formatTime` looks like the option for that and is not. The
upstream typings declare it, but lightweight-charts 5.2.1 never reads it,
so setting it changes nothing. Passing it here logs a warning pointing at
`localization.timeFormatter` rather than failing silently.

There is no `timeScale.tickMarkFormatter` here either; that option belongs
to time charts. Every other `timeScale` option applies unchanged.}

\item{click}{Logical | numeric | character | named list | unnamed list. Last-clicked chart position; read-only. Same shape as `crosshair`.
Written only when `subscribeClick` is true.}

\item{crosshair}{Logical | numeric | character | named list | unnamed list. Crosshair position; read-only. Carries `time`, `logical`, `paneIndex`,
`point`, `seriesData` and `price` keyed by series id, `hoveredSeriesId`
and `hoveredObjectId`. `seriesData` holds whole data points and is
present only for series with data under the cursor; `price` is the price
at the cursor on each series' own scale and is defined between bars too.
Written only when `subscribeCrosshair` is true.}

\item{crosshairPosition}{Logical | numeric | character | named list | unnamed list. Places the crosshair without a pointer, for syncing one chart to another.
`None` clears it. Positioning this way deliberately does not emit a
`crosshair` report, so two charts pointed at each other cannot loop.}

\item{dataAction}{Logical | numeric | character | named list | unnamed list. Asks a series about its own data, answering on `dataResult`.

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
repeat a query.}

\item{dataResult}{Logical | numeric | character | named list | unnamed list. Answer to the last `dataAction`; read-only. Always carries the `action`
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
two apart.}

\item{dblClick}{Logical | numeric | character | named list | unnamed list. Last double-clicked chart position; read-only. Same shape as `crosshair`.
Written only when `subscribeDblClick` is true.}

\item{fullChartOptions}{Logical | numeric | character | named list | unnamed list. Full chart options including defaults; read-only.}

\item{fullPriceScaleOptions}{Logical | numeric | character | named list | unnamed list. Full options of the chart's default visible price scale, including
defaults; read-only. That is the right scale on most charts, but the left
one wherever only the left is visible, which is how a yield curve chart
ships.}

\item{fullSeriesOptions}{Logical | numeric | character | named list | unnamed list. Full series options including defaults, keyed by series id; read-only.}

\item{fullTimeScaleOptions}{Logical | numeric | character | named list | unnamed list. Full horizontal scale options including defaults; read-only.}

\item{height}{Character | numeric. Sets height of the parent div of the chart.}

\item{paneOptions}{List of lists containing elements 'height', 'stretchfactor'.
those elements have the following types:
  - height (numeric; optional): fixed height in pixels. mutually exclusive with `stretchfactor`, because
the library implements a fixed height by rewriting every pane's stretch
factor. ignored when the chart has only one pane.
  - stretchfactor (numeric; optional): share of the remaining space, relative to the other panes. proportional
sizing survives a resize where a fixed height does not, so prefer it on a
responsive page.s. Pane sizing, positional by pane index. Panes come into existence through
`series[].pane`; this only sizes them.}

\item{priceScaleWidth}{Numeric. Width in pixels of the chart's default visible price scale; read-only.
Picked the same way as `fullPriceScaleOptions`. Reported on scale resize
only when `subscribeSize` is true.}

\item{reportThrottle}{Numeric. Milliseconds to coalesce reports over, applied to every `subscribe*`
stream. Zero batches to one report per animation frame.}

\item{screenshot}{Character. The most recent screenshot as a PNG data URI; read-only. Written once per
change of `screenshotRequest`.}

\item{screenshotRequest}{Numeric. Increment to capture the chart; the PNG arrives as a data URI on the
`screenshot` prop. An integer counter such as a button's `n_clicks` is
the intended shape, and `0` means no request.

The capture excludes the crosshair. An image watermark loaded from
another origin taints the canvas and makes the export fail, so serve one
with CORS headers if screenshots matter.}

\item{series}{List of lists containing elements 'id', 'type', 'data', 'options', 'pricescaleoptions', 'markers', 'pricelines', 'updownmarkers', 'pane'.
those elements have the following types:
  - id (character; required): stable identity for this series. used to key incremental updates and to
key the `crosshair`, `click` and `fullseriesoptions` payloads.
  - type (a value equal to: 'area', 'line'; required): which kind of series to draw. the names this chart accepts are the ones
listed on this field's type; `bar` and `candlestick` need ohlc points,
and the rest take a single `value`.
  - data (list of logical | numeric | character | named list | unnamed lists; required): data points. items carrying only `time` are whitespace and render as gaps.
  - options (logical | numeric | character | named list | unnamed list; optional): series options. see the `seriesoptionscommon` interface of the underlying
charting library, plus the options specific to this series type.
  - pricescaleoptions (logical | numeric | character | named list | unnamed list; optional): options for the price scale this series is attached to. this is where
`scalemargins` lives; it is not a series option.
  - markers (logical | numeric | character | named list | unnamed list; optional): markers drawn against this series.
  - pricelines (logical | numeric | character | named list | unnamed list; optional): horizontal price lines drawn against this series.
  - updownmarkers (logical | numeric | character | named list | unnamed list; optional): up and down markers: a temporary marker coloured by whether a revised
value rose or fell. options are `positivecolor`, `negativecolor` and
`updatevisibilityduration`; pass an empty object for the defaults, or
omit the key for no markers. line and area series only.

a marker appears only when a `tick` revises a bar the plugin already
knows about, and it only learns bars through the series `data`. a tick
that appends a new bar therefore draws nothing, and repeated revisions of
the same bar are all coloured against the value that arrived in `data`,
not against the previous tick.
  - pane (numeric; optional): index of the pane this series is drawn on, counting from 0. panes stack
vertically and share one horizontal scale. an index one past the last
pane creates a pane; further than that is clamped by the library, so keep
the indices contiguous. panes with no series are kept rather than
collapsed, so that these indices, and `paneoptions`, stay stable.s. The series drawn on this chart, each carrying its own id, type, data,
options, markers and price lines.}

\item{subscribeClick}{Logical. Whether to report chart clicks through the `click` prop.}

\item{subscribeCrosshair}{Logical. Whether to report crosshair movement through the `crosshair` prop. Off by
default: every report is a network round trip, and crosshair movement
fires on every mouse move.}

\item{subscribeDblClick}{Logical. Whether to report double clicks through the `dblClick` prop.}

\item{subscribeSize}{Logical. Whether to report scale dimensions through `timeScaleWidth`,
`timeScaleHeight` and `priceScaleWidth`. Off by default: `autoSize`
drives these from a resize observer, so they fire every frame while the
window is being dragged.}

\item{subscribeVisibleRange}{Logical. Whether to report scale range changes through `visibleRange` and
`visibleLogicalRange`. Off by default: these fire continuously while
panning and zooming.}

\item{tick}{Logical | numeric | character | named list | unnamed list. Appends a bar to a series without replacing its data, which is what keeps
the visible range steady while streaming. Accepts one tick or a list, so
a batch of bars costs one prop write.

Because this is a prop rather than an event, a tick identical to the
previous one does not re-fire. A tick naming an unknown series id is
ignored with a console warning, since it can arrive before the callback
that creates the series.}

\item{timeScaleAction}{Logical | numeric | character | named list | unnamed list. Runs a one-off horizontal scale command: `fitContent`,
`scrollToRealTime`, `resetTimeScale` or `scrollToPosition`. The value is
compared by content, so re-emitting the same command from an unrelated
callback does nothing; change the `nonce` to ask for a genuine repeat.}

\item{timeScaleHeight}{Numeric. Height of the horizontal scale in pixels; read-only. Written only when
`subscribeSize` is true.}

\item{timeScaleWidth}{Numeric. Width of the horizontal scale in pixels; read-only. Written only when
`subscribeSize` is true.}

\item{visibleLogicalRange}{Logical | numeric | character | named list | unnamed list. Visible range in bar indices, as `{from, to}`. Two-way, like
`visibleRange`, and reported only while `subscribeVisibleRange` is true.
Indices may be fractional, and may fall outside the data. Setting both
this and `visibleRange` in one callback is ambiguous; this one wins.}

\item{visibleRange}{Logical | numeric | character | named list | unnamed list. Visible range, as `{from, to}` in the same form the series data uses.
Two-way: set it to move the chart, and read it to follow the user, though
it is only reported while `subscribeVisibleRange` is true. The library
clamps a requested range to the data that exists, so what is reported
back will often not equal what was set.}

\item{watermark}{Logical | numeric | character | named list | unnamed list. Draws a watermark over a pane. Give `imageUrl` for an image, or `lines`
for text. `None` removes it.}

\item{width}{Character | numeric. Sets width of the parent div of the chart.}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

