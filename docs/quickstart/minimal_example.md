# Your first chart

The smallest app that draws something.

## 1. Install

```
pip install dash_tvlwc
```

## 2. Write the app

```python
import dash
from dash import html
import dash_tvlwc

candlestick_data = [
    {'time': '2026-01-01', 'open': 100, 'high': 101.3, 'low': 95.1, 'close': 97.6},
    {'time': '2026-01-02', 'open': 97.6, 'high': 99.1, 'low': 95.2, 'close': 96.1},
    {'time': '2026-01-03', 'open': 96.1, 'high': 98.4, 'low': 90.7, 'close': 92.1},
    {'time': '2026-01-04', 'open': 92.1, 'high': 97.9, 'low': 89.8, 'close': 95.7},
    {'time': '2026-01-05', 'open': 95.7, 'high': 97.5, 'low': 88.6, 'close': 92.4},
]

line_data = [
    {'time': '2026-01-01', 'value': 100.4},
    {'time': '2026-01-02', 'value': 97.1},
    {'time': '2026-01-03', 'value': 95.7},
    {'time': '2026-01-04', 'value': 98.7},
    {'time': '2026-01-05', 'value': 100.3},
]

app = dash.Dash(__name__)
app.layout = html.Div([
    dash_tvlwc.Tvlwc(
        id='chart',
        series=[
            {'id': 'price', 'type': 'candlestick', 'data': candlestick_data},
            {'id': 'signal', 'type': 'line', 'data': line_data},
        ],
        width='100%',
        height=400,
        # With only a handful of points the default view sits at the right
        # edge and looks squashed. Fitting once on load spreads them across
        # the width. A few hundred bars need no such help.
        timeScaleAction={'action': 'fitContent', 'nonce': 1},
    ),
])

if __name__ == '__main__':
    app.run()
```

## 3. Run it

```
python app.py
```

The app is at `localhost:8050`, and looks like this:

![Two series on one chart](../_static/minimal_example.png)

## What to notice

**Each series is one dictionary.** `id`, `type` and `data` are required; add
more dictionaries to the list to draw more series on the same chart.

**The `id` is yours to choose**, and it matters. It is how the component knows
that the series you send next is the same one, so it can update it in place
rather than recreating it, and it is the key every callback payload uses to
refer to that series.

**Data is a list of dictionaries, sorted by `time`.** Candlesticks and bars take
`open`, `high`, `low`, `close`; every other type takes `value`.

**Times can be date strings, `{'year', 'month', 'day'}` dictionaries, or UTC
timestamps in seconds.** Pick one form per series and stay with it. Whatever you
send is what comes back in callback payloads.

## Next

- Colours, grids and axes: [Chart and series options](../options)
- Markers, price lines, sub-plots: [Series and data](../series)
- Making it react: [Callbacks](callback_example)
