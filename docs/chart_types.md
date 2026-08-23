# Chart types

Three components, one prop surface. They differ only in what the horizontal axis
measures, and which series types the underlying library allows on it.

```{list-table}
:header-rows: 1
:widths: 14 24 34 28

* - Component
  - Horizontal axis
  - `time` in a data point is
  - Series types
* - `Tvlwc`
  - Time
  - A date, or a UTC timestamp in seconds
  - All six
* - `Tvlwo`
  - Price
  - A price, such as an option strike
  - All six
* - `Tvlwy`
  - Maturity
  - A number of months
  - `line`, `area`
```

Every prop described elsewhere in these docs works the same on all three. A
callback written against one works against the others; only the meaning of
`time` changes.

## `Tvlwc`: a time axis

The ordinary case, covered throughout the rest of this documentation.

```python
dash_tvlwc.Tvlwc(
    series=[{'id': 'price', 'type': 'candlestick', 'data': candles}],
)
```

## `Tvlwo`: a price axis

For anything plotted against a price rather than against time: an option payoff,
an implied volatility smile, a depth curve.

```python
dash_tvlwc.Tvlwo(
    series=[{'id': 'iv', 'type': 'area', 'data': [
        {'time': 60,  'value': 25.1},
        {'time': 90,  'value': 19.4},
        {'time': 100, 'value': 18.0},
        {'time': 120, 'value': 21.6},
        {'time': 160, 'value': 24.3},
    ]}],
    chartOptions={'localization': {'precision': 0}},
    timeScaleAction={'action': 'fitContent', 'nonce': 1},
)
```

`time` is still called `time`, and it is now a strike. Points sit at their real
distance apart, so unevenly spaced strikes are drawn unevenly, which is the
whole reason to use this rather than a line chart.

`localization.precision` sets how many decimal places the axis labels carry. It
replaces `timeScale.tickMarkFormatter`, which time charts have and this one does
not.

:::{tip}
The default view is a window of points from the right edge, which on a price
axis rarely lands where you want. Fitting once on load is usually right for a
curve, where the whole domain is the point:
`timeScaleAction={'action': 'fitContent', 'nonce': 1}`.
:::

## `Tvlwy`: a maturity axis

For yield curves and term structures.

```python
dash_tvlwc.Tvlwy(
    series=[{'id': 'curve', 'type': 'line', 'data': [
        {'time': 1,   'value': 5.32},   # 1 month
        {'time': 12,  'value': 4.78},   # 1 year
        {'time': 120, 'value': 4.21},   # 10 years
        {'time': 360, 'value': 4.39},   # 30 years
    ]}],
    chartOptions={
        'yieldCurve': {'baseResolution': 1, 'minimumTimeRange': 120,
                       'startTimeRange': 0},
        'localization': {'timeFormatter': 'maturity'},
    },
    timeScaleAction={'action': 'fitContent', 'nonce': 1},
)
```

`time` is a number of `baseResolution` units, which default to months. One month
and thirty years sit at their real distance apart, so the short end stays
readable instead of being stretched to even steps.

The `yieldCurve` option group:

```{list-table}
:header-rows: 1
:widths: 26 16 58

* - Key
  - Default
  - Meaning
* - `baseResolution`
  - `1`
  - The smallest unit on the axis, in months.
* - `minimumTimeRange`
  - `120`
  - The least the axis will show, in those units, so a short curve does not fill
    the width.
* - `startTimeRange`
  - `0`
  - Where the axis begins.
```

Only `line` and `area` are accepted. Any other type is rejected with a message
naming the valid ones.

:::{warning}
To label the maturity axis, use `localization.timeFormatter`, naming a function
as described in [options](options.md#options-that-must-be-functions). It receives
the maturity in `baseResolution` units.

There is an option called `yieldCurve.formatTime` in the library's typings that
looks like the one for this. It is never read by Lightweight Charts 5.2.1, so
setting it does nothing. Passing it here logs a warning pointing at the option
that works.
:::

```javascript
/* assets/chart_functions.js */
window.dashTvlwcFunctions = window.dashTvlwcFunctions || {};
window.dashTvlwcFunctions.maturity = function (months) {
    if (months < 12) { return months + 'M'; }
    return (months / 12) + 'Y';
};
```
