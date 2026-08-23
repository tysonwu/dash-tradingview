# Migrating from 0.1.x

0.2.0 replaces five positionally-aligned lists with one list of dictionaries,
and moves from Lightweight Charts 3.8 to 5.2.1. Existing apps need editing.

## The one change that matters

**Before**, a series was spread across five props, matched up by position:

```python
dash_tvlwc.Tvlwc(
    seriesData=[candlestick_data, line_data],
    seriesTypes=['candlestick', 'line'],
    seriesOptions=[{'upColor': 'green'}, {'color': 'blue'}],
    seriesMarkers=[[], [marker]],
    seriesPriceLines=[[], [line]],
)
```

**Now**, a series is one dictionary:

```python
dash_tvlwc.Tvlwc(
    series=[
        {'id': 'price', 'type': 'candlestick', 'data': candlestick_data,
         'options': {'upColor': 'green'}},
        {'id': 'signal', 'type': 'line', 'data': line_data,
         'options': {'color': 'blue'}, 'markers': [marker],
         'priceLines': [line]},
    ],
)
```

The `id` is new and required. It replaces list position as the way a series is
identified, which is what makes incremental updates and per-series payloads
possible.

## Prop by prop

```{list-table}
:header-rows: 1
:widths: 34 66

* - 0.1.x
  - 0.2.0
* - `seriesData`
  - `series[].data`
* - `seriesTypes`
  - `series[].type`
* - `seriesOptions`
  - `series[].options`
* - `seriesMarkers`
  - `series[].markers`
* - `seriesPriceLines`
  - `series[].priceLines`
* - `chartOptions`
  - `chartOptions`, unchanged
* - `width`, `height`
  - unchanged
* - `crosshair`, `click`
  - Same names, richer payload. `seriesData` inside them is now keyed by your
    series `id` instead of by list index.
* - `timeRangeVisibleRange`
  - `visibleRange`, and now two-way
* - `timeRangeVisibleLogicalRange`
  - `visibleLogicalRange`, and now two-way
* - `fullChartOptions`, `fullPriceScaleOptions`, `fullTimeScaleOptions`
  - unchanged
* - `timeScaleWidth`, `timeScaleHeight`
  - unchanged, but now behind `subscribeSize`
```

## Reporting is now opt-in

In 0.1.x, crosshair and click were always reported. Every report is a network
round trip, and on a hosted app that was a request per pointer move.

They are now off unless asked for:

```python
dash_tvlwc.Tvlwc(
    subscribeCrosshair=True,
    subscribeClick=True,
    reportThrottle=50,
)
```

If a callback of yours stopped firing after upgrading, this is why.

## Formatters are no longer JavaScript source strings

**Before**, a formatter was a string of JavaScript that the component ran
through `eval`:

```python
chartOptions={'localization': {
    'priceFormatter': "(function(price) { return '$' + price.toFixed(2); })"
}}
```

**Now**, register the function in your `assets/` folder and name it:

```javascript
/* assets/chart_functions.js */
window.dashTvlwcFunctions = window.dashTvlwcFunctions || {};
window.dashTvlwcFunctions.usd = function (price) {
    return '$' + price.toFixed(2);
};
```

```python
chartOptions={'localization': {'priceFormatter': 'usd'}}
```

A name that is not registered raises immediately, saying which option asked for
it.

## Options that moved in the library

Between 3.8 and 5.2.1 the upstream library moved some options. The ones most
likely to be in an existing app:

```{list-table}
:header-rows: 1
:widths: 44 56

* - Was
  - Now
* - `series[].options.scaleMargins`
  - `series[].priceScaleOptions.scaleMargins`
* - `chartOptions.watermark`
  - The `watermark` prop
* - `chartOptions.layout.backgroundColor`
  - `chartOptions.layout.background`, as `{'type': 'solid', 'color': ...}`
* - `chartOptions.timeScale.drawTicks`
  - `chartOptions.timeScale.ticksVisible`
```

`scaleMargins` is the one that bites, because it silently does nothing in its
old position. If your volume histogram now fills the pane, that is this.

For anything not listed, the upstream migration guides are authoritative:
[v3 to v4](https://tradingview.github.io/lightweight-charts/docs/migrations/from-v3-to-v4)
and
[v4 to v5](https://tradingview.github.io/lightweight-charts/docs/migrations/from-v4-to-v5).

## A worked upgrade

```{code-block} python
:caption: 0.1.x

dash_tvlwc.Tvlwc(
    id='chart',
    seriesData=[ohlc, volume],
    seriesTypes=['candlestick', 'histogram'],
    seriesOptions=[
        {'upColor': '#26a69a', 'downColor': '#ef5350'},
        {'priceFormat': {'type': 'volume'}, 'priceScaleId': '',
         'scaleMargins': {'top': 0.8, 'bottom': 0}},
    ],
    chartOptions={'layout': {'backgroundColor': '#ffffff'}},
)
```

```{code-block} python
:caption: 0.2.0

dash_tvlwc.Tvlwc(
    id='chart',
    series=[
        {'id': 'price', 'type': 'candlestick', 'data': ohlc,
         'options': {'upColor': '#26a69a', 'downColor': '#ef5350'}},
        {'id': 'volume', 'type': 'histogram', 'data': volume,
         'options': {'priceFormat': {'type': 'volume'}, 'priceScaleId': ''},
         'priceScaleOptions': {'scaleMargins': {'top': 0.8, 'bottom': 0}}},
    ],
    chartOptions={'layout': {'background': {'type': 'solid',
                                            'color': '#ffffff'}}},
)
```

Three edits: the five lists became one, `scaleMargins` moved to
`priceScaleOptions`, and `backgroundColor` became `background`.

## What you gain

Things that were not possible in 0.1.x and need no migration to start using:
stacked panes, streaming with `tick`, setting the visible range, placing the
crosshair, removing a price line, double-click, watermarks, screenshots,
reading data back, and the `Tvlwo` and `Tvlwy` chart types. See
[callbacks](callbacks) and [chart types](chart_types).
