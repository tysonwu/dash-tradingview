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
- `data` (optional): The data for the series. data has the following type: Array of lists containing elements 'seriesData', 'seriesType', 'seriesOptions'.
Those elements have the following types:
  - `seriesData` (Array of Dicts; optional)
  - `seriesType` (a value equal to: 'bar', 'candlestick', 'area', 'baseline', 'line', 'histogram'; optional)
  - `seriesOptions` (Dict; optional)s
- `height` (String | Real; optional): Sets height of the parent div of the chart
- `width` (String | Real; optional): Sets width of the parent div of the chart
"""
function tvlwc(; kwargs...)
        available_props = Symbol[:id, :chartOptions, :data, :height, :width]
        wild_props = Symbol[]
        return Component("tvlwc", "Tvlwc", "dash_tvlwc", available_props, wild_props; kwargs...)
end

