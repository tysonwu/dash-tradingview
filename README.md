<div align="center">

# 📊 dash-tvlwc

**Financial charts for [Dash](https://dash.plotly.com/), written in Python.**

A Dash component that wraps [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts), so you can build candlestick, line, area and volume charts without writing any JavaScript.

[Live demo](http://tysonwu.pythonanywhere.com/) · [Documentation](https://dash-tradingview.readthedocs.io/) · [PyPI](https://pypi.org/project/dash-tvlwc/)

</div>

---

## Why this and not a general plotting library

Lightweight Charts is built for one job: price series that stay smooth while you pan, zoom and stream into them. It handles very large series at 60fps, which general-purpose plotting libraries are not designed for.

This package makes it an ordinary Dash component. You describe the chart with Python dictionaries, and you read and drive it with ordinary Dash callbacks.

## Install

```
pip install dash_tvlwc
```

## Your first chart

```python
import dash
from dash import html
import dash_tvlwc

candles = [
    {'time': '2026-01-01', 'open': 100, 'high': 101.3, 'low': 95.1, 'close': 97.6},
    {'time': '2026-01-02', 'open': 97.6, 'high': 99.1, 'low': 95.2, 'close': 96.1},
    {'time': '2026-01-03', 'open': 96.1, 'high': 98.4, 'low': 90.7, 'close': 92.1},
]

app = dash.Dash(__name__)
app.layout = html.Div([
    dash_tvlwc.Tvlwc(
        series=[{'id': 'price', 'type': 'candlestick', 'data': candles}],
        width='100%',
        height=400,
    ),
])

if __name__ == '__main__':
    app.run()
```

Each series is one dictionary carrying its own `id`, `type` and `data`. Put several in the list to draw several series on one chart.

## What you can do

Each of these is an ordinary prop, set or read from a callback.

| | |
| --- | --- |
| **Six series types** | candlestick, bar, line, area, baseline, histogram |
| **Sub-plots** | stack panes that share one time axis, for price over volume over an indicator |
| **Live streaming** | append or revise a single bar without resending the whole series |
| **Mouse events** | crosshair, click and double-click, reported with the time and price under the cursor |
| **Drive the view** | set the visible range, scroll, fit to content, or place the crosshair from Python |
| **Sync two charts** | point them at each other so hovering one moves the other |
| **Infinite history** | be told when the user scrolls past the start of the data, and send more |
| **Markers and price lines** | anchored to a bar or to a price |
| **Read data back** | ask a series for one bar, or for its last value, without shipping the dataset |
| **Screenshots** | capture the canvas as a PNG |
| **Three chart types** | a time axis (`Tvlwc`), a price axis (`Tvlwo`), a maturity axis (`Tvlwy`) |

## What it cannot do

This is a bridge between Python and a JavaScript charting library, and some things do not survive the crossing:

- **Anything that has to be a function** - custom scaling logic, colour parsers, axis formatters written in Python. Formatters are still possible, but you write them in a small JavaScript file and refer to them by name.
- **Plugins, custom series types and drawing tools.** These are JavaScript classes in the underlying library, and a class cannot be expressed as a Dash prop.
- **Anything that must react within a single frame**, such as dragging a trendline. Every interaction routed through a Python callback costs a network round trip.
- **Reading a whole dataset back out of the chart.** You can ask for one point at a time; you cannot ask for all of them.

The documentation has [a page on each of these](https://dash-tradingview.readthedocs.io/en/latest/limitations.html) and what to do instead.

## Documentation

- **[Documentation site](https://dash-tradingview.readthedocs.io/)** - how to express a chart in Python, with worked examples.
- **[Lightweight Charts v5 API](https://tradingview.github.io/lightweight-charts/docs)** - the full list of chart and series options. Whatever the library accepts, this component passes through.
- **[`demo/app.py`](./demo/app.py)** - source of the [live demo](http://tysonwu.pythonanywhere.com/); every panel shows the settings behind it.
- **[`examples/`](./examples/)** - runnable apps for styling, callbacks and each capability.

## Compatibility

| | |
| --- | --- |
| Python | 3.9 or newer |
| Dash | 3.0 or newer, tested to 4.4 |
| Lightweight Charts | 5.2.1, bundled |

Version 0.2.0 changes the prop schema. Upgrading from 0.1.x is covered by the [migration guide](https://dash-tradingview.readthedocs.io/en/latest/migration.html).

## Contributing

Bug reports and pull requests are welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md), and [DEVELOPMENT.md](./DEVELOPMENT.md) for building the component from source.

## License

MIT. Charts by [TradingView](https://www.tradingview.com/), used under the Apache 2.0 license of Lightweight Charts.
