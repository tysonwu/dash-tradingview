# Callbacks

Everything interactive happens through props. There are four kinds, and telling
them apart is most of what there is to learn.

```{list-table}
:header-rows: 1
:widths: 22 78

* - Kind
  - How it behaves
* - **Describing props**
  - `series`, `chartOptions`, `paneOptions`, `watermark`. You set them; they say
    what the chart *is*. Send the whole value, not a patch.
* - **Reporting props**
  - `crosshair`, `click`, `barsInLogicalRange`, `dataResult`. Read-only. The
    component writes them; you use them as callback `Input`s.
* - **Command props**
  - `timeScaleAction`, `dataAction`, `screenshotRequest`. You set them to ask
    for something to happen once.
* - **Two-way props**
  - `visibleRange`, `visibleLogicalRange`. Set them to move the chart, read them
    to follow the user.
```

## Reporting: reading the chart

Every report is a network round trip, so **they are all off by default**. Turn
on the ones you need:

```python
dash_tvlwc.Tvlwc(
    id='chart',
    series=[{'id': 'price', 'type': 'candlestick', 'data': candles}],
    subscribeCrosshair=True,
    reportThrottle=50,
)
```

```{list-table}
:header-rows: 1
:widths: 32 68

* - Switch
  - Turns on
* - `subscribeCrosshair`
  - `crosshair`, on every pointer move
* - `subscribeClick`
  - `click`
* - `subscribeDblClick`
  - `dblClick`
* - `subscribeVisibleRange`
  - `visibleRange`, `visibleLogicalRange`, `barsInLogicalRange`
* - `subscribeSize`
  - `priceScaleWidth`, `timeScaleWidth`, `timeScaleHeight`
```

`reportThrottle` is a number of milliseconds to coalesce reports over. `0`
batches to one report per animation frame. Crosshair movement and panning fire
continuously, so leaving this at zero on a hosted app means a request per frame.
Something like `50` to `100` is usually the right trade.

### The mouse payload

`crosshair`, `click` and `dblClick` all carry the same shape:

```python
@callback(Output('readout', 'children'), Input('chart', 'crosshair'))
def show(payload):
    if not payload or payload.get('time') is None:
        return 'Hover the chart'
    bar = payload['seriesData'].get('price')     # keyed by YOUR series id
    price = payload['price'].get('price')        # price under the cursor
    return f"{payload['time']}: {bar['close']} (cursor at {price:.2f})"
```

```{list-table}
:header-rows: 1
:widths: 26 74

* - Key
  - Meaning
* - `time`
  - The time under the cursor, in the same form your data used. `None` outside
    the data range, which is worth checking first.
* - `logical`
  - The bar index under the cursor. May be fractional, and may fall outside the
    data.
* - `seriesData`
  - The whole data point under the cursor, keyed by series id. A series with no
    point there is simply absent from the dictionary.
* - `price`
  - The price at the cursor on each series' own scale, keyed by series id.
    Unlike `seriesData` this is defined between bars, which is what makes
    click-to-annotate possible.
* - `paneIndex`
  - Which stacked pane the cursor is in.
* - `point`
  - Pixel coordinates, `{'x': ..., 'y': ...}`.
* - `hoveredSeriesId`
  - The series under the cursor, if any.
```

:::{note}
A double-click fires `click` **and** `dblClick` in the same batch, so
`ctx.triggered_id` cannot tell them apart. If you handle both, scan
`ctx.triggered` and let `dblClick` win.
:::

## Commands: making something happen once

A command prop is a request, not a state. The catch is that Dash props only
notify on *change*, so asking for the same thing twice needs something to
differ. Every command prop takes a `nonce` for that, and a button's `n_clicks`
is the natural thing to put in it.

```python
@callback(
    Output('chart', 'timeScaleAction'),
    Input('fit', 'n_clicks'),
    prevent_initial_call=True,
)
def fit(n_clicks):
    return {'action': 'fitContent', 'nonce': n_clicks}
```

Without the nonce, the second press sends a value identical to the first, and
nothing happens.

`timeScaleAction` takes `fitContent`, `scrollToRealTime`, `resetTimeScale` and
`scrollToPosition` (with `position` and `animated`).

`screenshotRequest` is simpler: it is an integer, and any change captures the
canvas. The PNG arrives on `screenshot` as a data URI.

```python
@callback(Output('chart', 'screenshotRequest'), Input('shot', 'n_clicks'))
def capture(n_clicks):
    return n_clicks

@callback(Output('preview', 'src'), Input('chart', 'screenshot'))
def show(data_uri):
    return data_uri
```

## Streaming with `tick`

Rewriting `series` on a timer sends the entire history on every update and
resets the view. `tick` appends a single bar instead:

```python
@callback(
    Output('chart', 'tick'),
    Input('timer', 'n_intervals'),
    State('store', 'data'),
)
def stream(n_intervals, state):
    return {'id': 'price', 'bar': {'time': state['next_time'],
                                   'open': o, 'high': h, 'low': l, 'close': c}}
```

- A bar whose `time` is after the last one is **appended**.
- A bar whose `time` **matches** the last one **replaces** it, which is how a
  live candle is revised in place while it forms.
- `historicalUpdate: True` amends a bar further back. It cannot insert a bar
  that does not already exist.
- Pass a list instead of one dictionary to send several bars in one write.

The visible range does not move when you append, so a user who has scrolled back
stays where they were.

`tick` leaves the chart holding more than `series[].data` describes. That is
deliberate, and the next callback that writes `series` makes the prop the whole
truth again.

## Reading data back

The chart holds your data, but you cannot ask for all of it (see
[limitations](limitations)). You can ask about one point at a time, through a
command in and a result out:

```python
@callback(
    Output('chart', 'dataAction'),
    Input('ask', 'n_clicks'),
    prevent_initial_call=True,
)
def ask(n_clicks):
    return {'action': 'lastValue', 'seriesId': 'price',
            'globalLast': True, 'nonce': n_clicks}

@callback(Output('out', 'children'), Input('chart', 'dataResult'))
def show(result):
    if not result or result['noData']:
        return 'no data'
    return f"{result['price']:.2f}"
```

Three actions:

- `dataByIndex` with a `logicalIndex` reads one bar. Add
  `mismatchDirection` (`nearestLeft`, `none`, `nearestRight`) to say what should
  happen when no bar sits exactly there.
- `lastValue` reads the last price and the colour it is drawn in.
- `pop` with a `count` removes bars from the end and reports what it removed,
  newest first. It is the counterpart to `tick`: trim without resending.

`dataResult` always carries the `action` and `seriesId` it answers, so one
callback can serve several queries.

## Two-way props: the visible range

`visibleRange` and `visibleLogicalRange` work in both directions. Set one to
move the chart:

```python
@callback(Output('chart', 'visibleRange'), Input('zoom', 'n_clicks'))
def zoom(n):
    return {'from': '2026-02-01', 'to': '2026-03-01'}
```

and read it, with `subscribeVisibleRange=True`, to follow the user. The
component ignores a value it has just reported, so a callback that echoes the
range back does not fight the user's pan.

The library clamps a requested range to the data that exists, so what comes back
often is not what you set.

`visibleRange` is in times; `visibleLogicalRange` is in bar indices, which may be
fractional and may fall outside the data. Setting both in one callback is
ambiguous, and the logical one wins.

## Infinite history

`barsInLogicalRange` reports how much data lies either side of the view, as a
small fixed-size payload. A negative `barsBefore` means the user has scrolled
past the start:

```python
@callback(
    Output('chart', 'series'),
    Output('loaded', 'data'),
    Input('chart', 'barsInLogicalRange'),
    State('loaded', 'data'),
    prevent_initial_call=True,
)
def page(bars, loaded):
    if not bars or bars['barsBefore'] > 20:
        raise PreventUpdate
    loaded = min(loaded + 200, len(HISTORY))
    return [{'id': 'price', 'type': 'candlestick',
             'data': HISTORY[-loaded:]}], loaded
```

Only a window of the data is ever in the browser. The rest stays on the server
until it is scrolled to.

## Syncing two charts

Point each chart's `crosshair` at the other's `crosshairPosition`:

```python
@callback(
    Output('chart-b', 'crosshairPosition'),
    Output('chart-a', 'crosshairPosition'),
    Input('chart-a', 'crosshair'),
    Input('chart-b', 'crosshair'),
    prevent_initial_call=True,
)
def sync(a, b):
    source = a if ctx.triggered_id == 'chart-a' else b
    if not source or source.get('time') is None:
        return None, None
    target = {'seriesId': 'price', 'time': source['time'],
              'price': source['price']['price']}
    if ctx.triggered_id == 'chart-a':
        return target, no_update
    return no_update, target
```

This looks like it should loop, and does not. Placing the crosshair from Python
deliberately does not emit a `crosshair` report, and Dash's dependency graph
keys on component *and* property, so `a.crosshair -> b.crosshairPosition` and
`b.crosshair -> a.crosshairPosition` are not a cycle.

It does cost a round trip per pointer move, so the follower lags on a hosted
app. A [clientside callback](https://dash.plotly.com/clientside-callbacks) with
the same wiring is instant, at the cost of writing it in JavaScript.

## A note on cost

Each of these props is a network round trip. That is fine for clicks and
buttons, and it is the reason the subscriptions are opt-in and throttled. Any
interaction that has to feel immediate under the cursor is better done
clientside; see [limitations](limitations).
