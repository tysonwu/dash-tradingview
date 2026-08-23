# Chart and series options

Options are the part of this package that is purest pass-through. Whatever
Lightweight Charts accepts, the component hands over unchanged, so the
authority on *what exists* is the upstream documentation:

- [ChartOptions](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptionsBase)
- [Series options common to all types](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesOptionsCommon)
- [Candlestick](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/CandlestickStyleOptions) ·
  [Bar](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/BarStyleOptions) ·
  [Line](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/LineStyleOptions) ·
  [Area](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/AreaStyleOptions) ·
  [Baseline](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/BaselineStyleOptions) ·
  [Histogram](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/HistogramStyleOptions)

This page is about translating those pages into Python.

## The translation rule

A nested option in the library's documentation becomes a nested dictionary, with
the same key names. Nothing is renamed, and nothing is flattened.

```{list-table}
:header-rows: 1
:widths: 50 50

* - In the library's docs
  - In Python
* - `layout.background.color`
  - `{'layout': {'background': {'color': '#ffffff'}}}`
* - `timeScale.timeVisible`
  - `{'timeScale': {'timeVisible': True}}`
* - `rightPriceScale.borderColor`
  - `{'rightPriceScale': {'borderColor': '#cccccc'}}`
```

Key names stay in JavaScript's `camelCase`. They are not converted to
`snake_case`.

Values follow the ordinary Python-to-JSON mapping: `True` becomes `true`, `None`
becomes `null`, and a Python number becomes a JavaScript one.

```python
dash_tvlwc.Tvlwc(
    series=[{'id': 'price', 'type': 'candlestick', 'data': candles,
             'options': {'upColor': '#30d158', 'downColor': '#ff453a',
                         'borderVisible': False}}],
    chartOptions={
        'layout': {
            'background': {'type': 'solid', 'color': '#1b1e24'},
            'textColor': '#9aa1b1',
        },
        'grid': {
            'vertLines': {'color': 'rgba(74, 81, 98, 0.32)'},
            'horzLines': {'color': 'rgba(74, 81, 98, 0.32)'},
        },
        'timeScale': {'timeVisible': True, 'borderColor': '#4a5162'},
    },
)
```

### Chart options against series options

Which of the two a key belongs to is decided by the library, not by this
wrapper, and getting it wrong fails quietly.

- **`chartOptions`** covers the canvas: layout, grid, crosshair, the price and
  time scales, scroll and scale behaviour.
- **`series[].options`** covers one series: its colours, line width, price
  format, and which price scale it attaches to.

If an option has no effect, checking which interface actually declares it is
usually the fastest diagnosis.

## Enumerated values

Some library options take an enum, which crosses the boundary as its underlying
value. `dash_tvlwc.types` mirrors the useful ones so you do not have to remember
which integer means what:

```python
from dash_tvlwc.types import LineStyle, CrosshairMode, PriceScaleMode

chartOptions={
    'crosshair': {'mode': CrosshairMode.Normal},
    'rightPriceScale': {'mode': PriceScaleMode.Logarithmic},
}
```

Using the plain value works identically. The enums exist for readability, not
because anything requires them.

Available: `ColorType`, `CrosshairMode`, `LastPriceAnimationMode`, `LineStyle`,
`LineType`, `PriceLineSource`, `PriceScaleMode`, `TickMarkType`,
`TrackingModeExitMode`, `MismatchDirection`, and `SeriesType`.

## Options that must be functions

A handful of options take a callback rather than a value: price formatters, time
formatters, tick mark formatters. **A function cannot cross a Dash prop**, which
is JSON, so these cannot be written in Python.

The way through is to register the function in JavaScript and refer to it by
name.

**1. Put a file in your Dash `assets/` folder.** Dash serves everything there
automatically.

```javascript
/* assets/chart_functions.js */
window.dashTvlwcFunctions = window.dashTvlwcFunctions || {};

window.dashTvlwcFunctions.usd = function (price) {
    return '$' + price.toFixed(2);
};

window.dashTvlwcFunctions.compact = function (value) {
    if (value >= 1e6) { return (value / 1e6).toFixed(1) + 'M'; }
    if (value >= 1e3) { return (value / 1e3).toFixed(1) + 'k'; }
    return value.toFixed(0);
};
```

**2. Name it from Python**, as a string, where the option expects a function.

```python
dash_tvlwc.Tvlwc(
    chartOptions={'localization': {'priceFormatter': 'usd'}},
    series=[{'id': 'vol', 'type': 'histogram', 'data': volume,
             'options': {'priceFormat': {'type': 'custom',
                                         'formatter': 'compact'}}}],
)
```

A name that is not registered raises immediately with a message saying which
option asked for it, rather than leaving you with a chart that is quietly wrong.

The options resolved this way are:

- `chartOptions.localization`: `priceFormatter`, `percentageFormatter`,
  `timeFormatter`, `tickmarksPriceFormatter`, `tickmarksPercentageFormatter`
- `chartOptions.timeScale.tickMarkFormatter` (time charts only)
- `series[].options.priceFormat`: `formatter`, `tickmarksFormatter`

:::{note}
This is an escape hatch, not a Python feature. The formatting logic is
JavaScript, and it runs in the browser. If your formatting depends on data or
state that only exists on the server, format the values in Python before
sending them and use a plain series instead.
:::

See [What this wrapper cannot do](limitations) for the options that have no
escape hatch at all.

## Reading the options back

Four read-only props report what the chart is actually using, defaults filled
in, which is the quickest way to find out whether an option landed:

```python
@callback(Output('out', 'children'), Input('chart', 'fullChartOptions'))
def show(options):
    return options['timeScale']['barSpacing']
```

`fullChartOptions`, `fullSeriesOptions` (keyed by series id),
`fullPriceScaleOptions` and `fullTimeScaleOptions` are written whenever options
change.

## Sizing

`width` and `height` size the `div` the chart is drawn into, and accept anything
CSS does:

```python
dash_tvlwc.Tvlwc(width='100%', height=400, ...)
```

The chart follows its container automatically when the window resizes. You do
not need to handle that yourself.
