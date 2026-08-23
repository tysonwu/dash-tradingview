# Making it react

The same chart, now reading the mouse and being driven from a callback.

```python
import dash
from dash import Input, Output, State, callback, ctx, html, no_update
import dash_tvlwc

candles = [
    {'time': '2026-01-01', 'open': 100, 'high': 101.3, 'low': 95.1, 'close': 97.6},
    {'time': '2026-01-02', 'open': 97.6, 'high': 99.1, 'low': 95.2, 'close': 96.1},
    {'time': '2026-01-03', 'open': 96.1, 'high': 98.4, 'low': 90.7, 'close': 92.1},
    {'time': '2026-01-04', 'open': 92.1, 'high': 97.9, 'low': 89.8, 'close': 95.7},
    {'time': '2026-01-05', 'open': 95.7, 'high': 97.5, 'low': 88.6, 'close': 92.4},
]

app = dash.Dash(__name__)
app.layout = html.Div([
    dash_tvlwc.Tvlwc(
        id='chart',
        series=[{'id': 'price', 'type': 'candlestick', 'data': candles}],
        width='100%',
        height=400,
        # Off by default: every report is a network round trip.
        subscribeCrosshair=True,
        subscribeClick=True,
        reportThrottle=50,
    ),
    html.Div(id='readout'),
    html.Button('Fit to content', id='fit', n_clicks=0),
])


@callback(Output('readout', 'children'), Input('chart', 'crosshair'))
def show_hover(payload):
    """Read the chart: what is under the cursor."""
    if not payload or payload.get('time') is None:
        return 'Hover the chart'
    bar = payload['seriesData'].get('price')
    if not bar:
        return f"{payload['time']}: no bar here"
    return f"{payload['time']}  O {bar['open']}  H {bar['high']}  " \
           f"L {bar['low']}  C {bar['close']}"


@callback(
    Output('chart', 'series'),
    Input('chart', 'click'),
    State('chart', 'series'),
    prevent_initial_call=True,
)
def annotate(click, series):
    """Drive the chart: draw a price line where the user clicked."""
    price = (click.get('price') or {}).get('price')
    if price is None:
        return no_update
    series[0]['priceLines'] = [{'price': price, 'title': 'clicked',
                                'axisLabelVisible': True}]
    return series


@callback(
    Output('chart', 'timeScaleAction'),
    Input('fit', 'n_clicks'),
    prevent_initial_call=True,
)
def fit(n_clicks):
    """Command the chart. n_clicks doubles as the nonce."""
    return {'action': 'fitContent', 'nonce': n_clicks}


if __name__ == '__main__':
    app.run()
```

## What to notice

**Reporting is opt-in.** `subscribeCrosshair` and `subscribeClick` are `False`
unless you say otherwise, because each report is a request to the server.
`reportThrottle` coalesces them; crosshair movement fires on every pointer move,
so leaving it at `0` on a hosted app means a request per frame.

**Payloads are keyed by your series `id`.** `payload['seriesData']['price']` is
the whole data point under the cursor. A series with no point there is simply
absent, so check before indexing.

**`price` and `seriesData` are different things.** `seriesData` is the bar, and
exists only where there is one. `price` is where the cursor is on that series'
scale, and exists between bars too, which is why the annotation callback uses
it.

**Driving the chart means sending the prop back.** There is no "add a price
line" method; you send the `series` value you want. The list is declarative, so
removing a line means sending the list without it.

**Commands need a nonce.** `timeScaleAction` is a request, not a state, and Dash
only notifies on change. Without something differing, the second press of the
button sends a value identical to the first and nothing happens. A button's
`n_clicks` is the natural nonce.

## Next

- Every prop and payload: [Callbacks](../callbacks)
- Streaming live data: [Streaming with `tick`](../callbacks.md#streaming-with-tick)
- What cannot be done this way: [Limitations](../limitations)
