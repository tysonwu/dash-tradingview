% Auto-generated: do not edit by hand
\name{tvlwc}

\alias{tvlwc}

\title{Tvlwc component}

\description{
Tradingview Lightweight Chart object
}

\usage{
tvlwc(id=NULL, chartOptions=NULL, click=NULL, crosshair=NULL,
fullChartOptions=NULL, fullPriceScaleOptions=NULL,
fullSeriesOptions=NULL, fullTimeScaleOptions=NULL,
height=NULL, priceScaleWidth=NULL, reportThrottle=NULL,
series=NULL, subscribeClick=NULL, subscribeCrosshair=NULL,
subscribeSize=NULL, subscribeVisibleRange=NULL,
timeScaleHeight=NULL, timeScaleWidth=NULL,
visibleLogicalRange=NULL, visibleRange=NULL, width=NULL)
}

\arguments{
\item{id}{Character. The ID of this component.}

\item{chartOptions}{Lists containing elements 'timescale', 'localization', 'width', 'height', 'autosize', 'layout', 'leftpricescale', 'rightpricescale', 'defaultvisiblepricescaleid', 'overlaypricescales', 'crosshair', 'grid', 'handlescroll', 'handlescale', 'kineticscroll', 'trackingmode', 'adddefaultpane', 'hoveredseriesontop'.
those elements have the following types:
  - timescale (logical | numeric | character | named list | unnamed list; optional): extended time scale options with option to override tickmarkformatter
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
@,defaultvalue,`true`. Object containing all chart options. Mirrors the `ChartOptions` interface
of the underlying charting library. Option values that must be functions,
such as `localization.priceFormatter`, are given as the string name of a
function registered on `window.dashTvlwcFunctions`.}

\item{click}{Logical | numeric | character | named list | unnamed list. Last-clicked chart position; read-only. Same shape as `crosshair`.
Written only when `subscribeClick` is true.}

\item{crosshair}{Logical | numeric | character | named list | unnamed list. Crosshair position; read-only. Carries `time`, `logical`, `paneIndex`,
`point`, `seriesData` and `price` keyed by series id, `hoveredSeriesId`
and `hoveredObjectId`. `seriesData` holds whole data points and is
present only for series with data under the cursor; `price` is the price
at the cursor on each series' own scale and is defined between bars too.
Written only when `subscribeCrosshair` is true.}

\item{fullChartOptions}{Logical | numeric | character | named list | unnamed list. Full chart options including defaults; read-only.}

\item{fullPriceScaleOptions}{Logical | numeric | character | named list | unnamed list. Full right price scale options including defaults; read-only.}

\item{fullSeriesOptions}{Logical | numeric | character | named list | unnamed list. Full series options including defaults, keyed by series id; read-only.}

\item{fullTimeScaleOptions}{Logical | numeric | character | named list | unnamed list. Full time scale options including defaults; read-only.}

\item{height}{Character | numeric. Sets height of the parent div of the chart.}

\item{priceScaleWidth}{Numeric. Width of the right price scale in pixels; read-only. Reported on scale
resize only when `subscribeSize` is true.}

\item{reportThrottle}{Numeric. Milliseconds to coalesce reports over, applied to every `subscribe*`
stream. Zero batches to one report per animation frame.}

\item{series}{List of lists containing elements 'id', 'type', 'data', 'options', 'pricescaleoptions', 'markers', 'pricelines'.
those elements have the following types:
  - id (character; required): stable identity for this series. used to key incremental updates and to
key the `crosshair`, `click` and `fullseriesoptions` payloads.
  - type (a value equal to: 'area', 'bar', 'baseline', 'candlestick', 'histogram', 'line'; required): one of `bar`, `candlestick`, `area`, `baseline`, `line`, `histogram`.
  - data (list of logical | numeric | character | named list | unnamed lists; required): data points. items carrying only `time` are whitespace and render as gaps.
  - options (logical | numeric | character | named list | unnamed list; optional): series options. see the `seriesoptionscommon` interface of the underlying
charting library, plus the options specific to this series type.
  - pricescaleoptions (logical | numeric | character | named list | unnamed list; optional): options for the price scale this series is attached to. this is where
`scalemargins` lives; it is not a series option.
  - markers (logical | numeric | character | named list | unnamed list; optional): markers drawn against this series.
  - pricelines (logical | numeric | character | named list | unnamed list; optional): horizontal price lines drawn against this series.s. The series drawn on this chart, each carrying its own id, type, data,
options, markers and price lines.}

\item{subscribeClick}{Logical. Whether to report chart clicks through the `click` prop.}

\item{subscribeCrosshair}{Logical. Whether to report crosshair movement through the `crosshair` prop. Off by
default: every report is a network round trip, and crosshair movement
fires on every mouse move.}

\item{subscribeSize}{Logical. Whether to report scale dimensions through `timeScaleWidth`,
`timeScaleHeight` and `priceScaleWidth`. Off by default: `autoSize`
drives these from a resize observer, so they fire every frame while the
window is being dragged.}

\item{subscribeVisibleRange}{Logical. Whether to report time scale range changes through `visibleRange` and
`visibleLogicalRange`. Off by default: these fire continuously while
panning and zooming.}

\item{timeScaleHeight}{Numeric. Height of the time scale in pixels; read-only. Written only when
`subscribeSize` is true.}

\item{timeScaleWidth}{Numeric. Width of the time scale in pixels; read-only. Written only when
`subscribeSize` is true.}

\item{visibleLogicalRange}{Logical | numeric | character | named list | unnamed list. Visible logical range in bar indices; read-only. Written only when
`subscribeVisibleRange` is true.}

\item{visibleRange}{Logical | numeric | character | named list | unnamed list. Visible time range; read-only. Written only when `subscribeVisibleRange`
is true.}

\item{width}{Character | numeric. Sets width of the parent div of the chart.}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

