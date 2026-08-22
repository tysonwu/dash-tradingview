# AUTO GENERATED FILE - DO NOT EDIT

export tvlwc

"""
    tvlwc(;kwargs...)

A Tvlwc component.
Tradingview Lightweight Chart object
Keyword arguments:
- `id` (String; optional): The ID of this component.
- `chartOptions` (optional): Object containing all chart options. Mirrors the `ChartOptions` interface
of the underlying charting library.. chartOptions has the following type: lists containing elements 'timeScale', 'localization', 'width', 'height', 'autoSize', 'layout', 'leftPriceScale', 'rightPriceScale', 'defaultVisiblePriceScaleId', 'overlayPriceScales', 'crosshair', 'grid', 'handleScroll', 'handleScale', 'kineticScroll', 'trackingMode', 'addDefaultPane', 'hoveredSeriesOnTop'.
Those elements have the following types:
  - `timeScale` (Bool | Real | String | Dict | Array; optional): Extended time scale options with option to override tickMarkFormatter
  - `localization` (Bool | Real | String | Dict | Array; optional): Localization options.
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
- `height` (String | Real; optional): Sets height of the parent div of the chart.
- `setProps` (optional): Dash-assigned callback that fires when a prop changes.
- `width` (String | Real; optional): Sets width of the parent div of the chart.
"""
function tvlwc(; kwargs...)
        available_props = Symbol[:id, :chartOptions, :height, :width]
        wild_props = Symbol[]
        return Component("tvlwc", "Tvlwc", "dash_tvlwc", available_props, wild_props; kwargs...)
end

