# dash-tvlwc

```{toctree}
:hidden:

quickstart/index
series
options
callbacks
chart_types
limitations
reference
migration
```

A [Dash](https://dash.plotly.com/) component wrapping
[TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts),
so financial charts can be built and driven entirely from Python.

Source on [Github](https://github.com/tysonwu/dash-tradingview), released on
[PyPI](https://pypi.org/project/dash-tvlwc/), with a
[live demo](http://tysonwu.pythonanywhere.com/).

## Install

```
pip install dash_tvlwc
```

Requires Python 3.9 or newer and Dash 3.0 or newer. Lightweight Charts 5.2.1 is
bundled; there is nothing to install on the JavaScript side.

## How to read this documentation

This package is a **wrapper**. Almost every visual question, which options exist,
what a candlestick series accepts, what `scaleMargins` does, is answered by the
underlying library, and its documentation is the right place to look:

- [Lightweight Charts v5 API reference](https://tradingview.github.io/lightweight-charts/docs/api)
- [ChartOptions](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptionsBase)
- [Series options](https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesOptionsCommon)

What that documentation cannot tell you is how any of it is **spelled in
Python**, or which parts survive the trip across a Dash prop at all. That is what
this site is for.

```{list-table}
:header-rows: 1
:widths: 30 70

* - Page
  - What it covers
* - [Quickstart](quickstart/index)
  - A first chart, then the same chart driven by a callback.
* - [Series and data](series)
  - The `series` prop: how a series is described, what a data point looks like,
    markers, price lines and panes.
* - [Chart and series options](options)
  - How library options map onto `chartOptions`, and what to do about options
    that must be JavaScript functions.
* - [Callbacks](callbacks)
  - Reading the chart, driving the chart, and streaming into it.
* - [Chart types](chart_types)
  - `Tvlwc`, `Tvlwo` and `Tvlwy`.
* - [What this wrapper cannot do](limitations)
  - The things that do not cross the Python boundary, and what to do instead.
* - [Prop reference](reference)
  - Every prop, in one table.
* - [Migrating from 0.1.x](migration)
  - The 0.2.0 prop schema, and what replaced what.
```

## The shape of it

One import, one component, and a list of dictionaries.

```python
import dash
from dash import html
import dash_tvlwc

app = dash.Dash(__name__)
app.layout = html.Div([
    dash_tvlwc.Tvlwc(
        id='chart',
        series=[{
            'id': 'price',
            'type': 'candlestick',
            'data': [
                {'time': '2026-01-01', 'open': 100, 'high': 101.3,
                 'low': 95.1, 'close': 97.6},
                {'time': '2026-01-02', 'open': 97.6, 'high': 99.1,
                 'low': 95.2, 'close': 96.1},
            ],
        }],
        width='100%',
        height=400,
    ),
])

if __name__ == '__main__':
    app.run()
```

Everything after this is variations on that: more entries in `series`, more keys
in `chartOptions`, and callbacks wired to the props that report and drive.
