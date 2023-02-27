# Reference

The Tradingview Lightweight Chart library (referred as *the original library* in below) is highly customizable in style. For the complete list of chart options and series options available, please refer to [the official API documentation](https://tradingview.github.io/lightweight-charts/docs/3.8).

```{note}
The supported version of Tradingview Lightweight Chart is v3.8.0. Make sure you consult the v3.8 document instead of latest version above 4.x.
```

## Dash Properties

**Configurable props**

|Property |Description  |
|---|---|
|`chartOptions`|a dict of options on chart canvas.|
|`seriesData`|a list series of list of timepoint dicts on series data.|
|`seriesTypes`|a list of series types, in the same order as `seriesData`.|
|`seriesOptions`|a list of series option dict for each series, in the same order as `seriesData`.|
|`seriesMarkers`|a list of list of markers dicts for each series, in the same order as `seriesData`.|
|`seriesPriceLines`|a list of list of price line dicts for each series, in the same order as `seriesData`.|
|`width`|width of outer container of the chart.|
|`height`|height of outer container of the chart.|

**Read-only props**

|Property |Description  |
|---|---|
|`id`|identifiable ID for the chart.|
|`crosshair`|position of last mouse hover on chart (crosshair coordinates).|
|`click`|position of last mouse click on chart (click coordinates).|
|`fullChartOptions`|full dict of applied chart options including default options.|
|`fullPriceScaleOptions`|full dict of applied series options including default options.|
|`timeRangeVisibleRange`|from-to dates of visible time range.|
|`timeRangeVisibleLogicalRange`|from-to numbers of visible time range.|
|`timeScaleWidth`|width of time scale.|
|`timeScaleHeight`|height of time scale.|
|`fullTimeScaleOptions`|full dict of applied time scale options including default options.|

## Series Configurations

```{note}
A chart can contain more than one series. Therefore, series configurations should be passed in the format of a list. The order of the specifications in the lists does matter.

For example, data at index 0 of the property `seriesData` will be rendered along with the optional configurations specified at index 0 of the property `seriesOptions` if any dict is given there.
```

### `seriesTypes`

Sets type of the plot. Example:
```python
# two series, first one being candlestick plot and second being single line plot
seriesTypes=['candlestick', 'line']
```
There are six possible plot types, namely: `bar`, `candlestick`, `area`, `baseline`, `line`, and `histogram`.

### `seriesData`

Sets the data of each series.

**Example**
```python
candlestick_data = [
    {'close': 97.56, 'high': 101.29, 'low': 95.07, 'open': 100, 'time': '2021-01-01'},
    {'close': 96.06, 'high': 99.06, 'low': 95.17, 'open': 97.56, 'time': '2021-01-02'},
    {'close': 92.06, 'high': 98.39, 'low': 90.72, 'open': 96.06, 'time': '2021-01-03'},
    {'close': 95.74, 'high': 97.87, 'low': 89.75, 'open': 92.06, 'time': '2021-01-04'}

line_data = [
    {'time': '2021-01-01', 'value': 100.35},
    {'time': '2021-01-02', 'value': 97.09},
    {'time': '2021-01-03', 'value': 95.74},
    {'time': '2021-01-04', 'value': 98.72}
]

seriesData = [candlestick_data, line_data]
```

Each of the timepoint data passed should contain a dict with keys `time`, `open`, `high`, `low`, `close` for the series of type `candlestick` and `bar`, and `time`, `value` for the other series types. Whitespace data (dates without values) is possible. Adding datapoint-specific color options is also possible for some series types. See [original documentation here](https://tradingview.github.io/lightweight-charts/docs/3.8/api/interfaces/SeriesDataItemTypeMap).

### `seriesMarkers`

Sets the additional markers associated with a particular series.

See [original documentation here](https://tradingview.github.io/lightweight-charts/docs/3.8/api/interfaces/SeriesMarker) for all possible markers options.

**Example**
```python
seriesMarkers = [[
    {'time': '2021-01-01', 'position': 'aboveBar', 'color': '#f68410', 'shape': 'circle', 'text': 'Signal'},
    {'time': '2021-01-02', 'position': 'belowBar', 'color': 'white', 'shape': 'arrowUp', 'text': 'Buy'}
]]
```

### `seriesPriceLines`

Sets the additional horizontal price lines associated with a particular series.

See [original documentation here](https://tradingview.github.io/lightweight-charts/docs/3.8/api/interfaces/PriceLineOptions) for all possible price lines options.

**Example**
```python
seriesPriceLines = [[{'price': 10, 'color': '#2962FF', 'lineStyle': 0, 'title': 'MAX PRICE', 'axisLabelVisible': True}]]
```

## Chart and Series Styling Options

### `chartOptions`

Sets options for the chart in general. `chartsData` is expected to be one(nested) dict that contains all chart options. One can explore the possible options in the [original documentation here](https://tradingview.github.io/lightweight-charts/docs/3.8/api/interfaces/ChartOptions).

```{note}
A very few chart options is not available due to non-serializability of that option in the original charting library.
Currently, the following configurations is not possible:
- Key `tickMarkFormatter` in `timescale` property.
```

Remarks: Keys `priceFormatter` and `tickFormatter` in `localization` property accepts a string of Javascript function as parameter. For example, `{'localization': {'priceFormatter': "(function(price) { return '$' + price.toFixed(2); })""}}` specifies prices on the chart to be displayed with a dollar sign and rounded to 2 decimal places. See [here](https://tradingview.github.io/lightweight-charts/docs/3.8/api#timeformatterfn) and [here](https://tradingview.github.io/lightweight-charts/docs/3.8/api#priceformatterfn) for more information on time formatter and price formatter.

### `seriesOptions`

Sets options for each of the series. `seriesOptions` is expected to be a list of (nested) dict that specifies option for each series. One can explore the possible options in the [original documentation here](https://tradingview.github.io/lightweight-charts/docs/3.8/api/interfaces/SeriesOptionsCommon).

The are extra possible options specific to each series types:
- [Extra options for type `bar`](https://tradingview.github.io/lightweight-charts/docs/3.8/api/interfaces/BarStyleOptions)
- [Extra options for type `candlestick`](https://tradingview.github.io/lightweight-charts/docs/3.8/api/interfaces/CandlestickStyleOptions)
- [Extra options for type `area`](https://tradingview.github.io/lightweight-charts/docs/3.8/api/interfaces/AreaStyleOptions)
- [Extra options for type `baseline`](https://tradingview.github.io/lightweight-charts/docs/3.8/api/interfaces/BaselineStyleOptions)
- [Extra options for type `line`](https://tradingview.github.io/lightweight-charts/docs/3.8/api/interfaces/LineStyleOptions)
- [Extra options for type `histogram`](https://tradingview.github.io/lightweight-charts/docs/3.8/api/interfaces/HistogramStyleOptions)

### `width`

Sets the width of the `div` associated with the chart.

### `height`

Sets the height of the `div` associated with the chart.

## Enums

Some useful enums provided in the original charting library are translated to Python Enum classes. The enum classes are included in this package. For example, by doing
```python
from dash_tvlwc.types import ColorType
```
you can represent chart the color types `'solid'` and `'gradient'` by `ColorType.Solid` and `ColorType.VerticalGradient` respectively. It is just optional to use these enum representations of strings in when setting chart properties, and you can achieve the same result by setting configurations in plain string. The existence of enums is just for developers who prefers enums for code organization.

```python
chart_options = {
    'layout': {
        'background': {
            'type': ColorType.Solid
        }
    }
}

# is equivalent to
chart_options = {
    'layout': {
        'background': {
            'type': 'solid'
        }
    }
}
```

Additionally, this package provides an enum class that is not found in the original charting library that deals with the series type:

```python
from dash_tvlwc.types import SeriesType

# set the seriesTypes
series_types = [SeriesType.Bar]
```

There are 6 possible enums for this additional class, which corresponds to the six types of series supported by the original chart library:

```python
class SeriesType(StrEnum):
    Bar = 'bar'
    Candlestick = 'candlestick'
    Area = 'area'
    Baseline = 'baseline'
    Line = 'line'
    Histogram = 'histogram'
```