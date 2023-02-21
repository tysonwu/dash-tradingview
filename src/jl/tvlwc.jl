# AUTO GENERATED FILE - DO NOT EDIT

export tvlwc

"""
    tvlwc(;kwargs...)

A Tvlwc component.
Tradingview Lightweight Chart object
Keyword arguments:
- `id` (String; optional): The ID of this component
- `chartOptions` (Dict; optional): Object containing all chart options
See https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions for possible options
- `click` (Dict; optional): Last-clicked on chart coordinates; read-only
- `crosshair` (Dict; optional): Crosshair coordinates; read-only
- `fullChartOptions` (Dict; optional): Full chart options including defaults; read-only
- `fullPriceScaleOptions` (Dict; optional): Full chart price scale options including defaults; read-only
- `fullSeriesOptions` (Array of Dicts; optional): Full series options including defaults; read-only
- `fullTimeScaleOptions` (Dict; optional): Full time scale options including defaults; read-only
- `height` (String | Real; optional): Sets height of the parent div of the chart
- `priceScaleWidth` (Real; optional): Width of price scale; read-only
- `seriesData` (Array of Array of Dictss; optional): Data for the series
- `seriesMarkers` (Array of Array of Dictss; optional): Additional markers for the series
- `seriesOptions` (Array of Dicts; optional): Options for the series
- `seriesPriceLines` (Array of Array of Dictss; optional): Additional price lines for the series
- `seriesTypes` (Array of a value equal to: 'bar', 'candlestick', 'area', 'baseline', 'line', 'histogram's; optional): Type of the series
- `timeRangeVisibleLogicalRange` (Dict; optional): Visible logical range; read-only
- `timeRangeVisibleRange` (Dict; optional): Visible time range; read-only
- `timeScaleHeight` (Real; optional): Height of time scale; read-only
- `timeScaleWidth` (Real; optional): Width of time scale; read-only
- `width` (String | Real; optional): Sets width of the parent div of the chart
"""
function tvlwc(; kwargs...)
        available_props = Symbol[:id, :chartOptions, :click, :crosshair, :fullChartOptions, :fullPriceScaleOptions, :fullSeriesOptions, :fullTimeScaleOptions, :height, :priceScaleWidth, :seriesData, :seriesMarkers, :seriesOptions, :seriesPriceLines, :seriesTypes, :timeRangeVisibleLogicalRange, :timeRangeVisibleRange, :timeScaleHeight, :timeScaleWidth, :width]
        wild_props = Symbol[]
        return Component("tvlwc", "Tvlwc", "dash_tvlwc", available_props, wild_props; kwargs...)
end

