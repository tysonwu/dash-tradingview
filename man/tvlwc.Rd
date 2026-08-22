% Auto-generated: do not edit by hand
\name{tvlwc}

\alias{tvlwc}

\title{Tvlwc component}

\description{
Tradingview Lightweight Chart object
}

\usage{
tvlwc(id=NULL, chartOptions=NULL, height=NULL, width=NULL)
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
of the underlying charting library.}

\item{height}{Character | numeric. Sets height of the parent div of the chart.}

\item{width}{Character | numeric. Sets width of the parent div of the chart.}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

