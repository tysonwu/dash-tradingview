# Series and data

Everything drawn on a chart comes from one prop: `series`, a list of
dictionaries. One dictionary is one series.

```python
dash_tvlwc.Tvlwc(
    series=[
        {'id': 'price', 'type': 'candlestick', 'data': candles},
        {'id': 'signal', 'type': 'line', 'data': line},
    ],
)
```

## The keys of a series

```{list-table}
:header-rows: 1
:widths: 22 78

* - Key
  - Meaning
* - `id`
  - **Required.** Your own name for this series. It has to be unique within the
    list, and it is the key every payload uses to talk about the series later,
    so pick something you will recognise in a callback.
* - `type`
  - **Required.** One of `bar`, `candlestick`, `area`, `baseline`, `line`,
    `histogram`.
* - `data`
  - **Required.** The points, described below.
* - `options`
  - Styling, passed straight to the library. See
    [Chart and series options](options).
* - `priceScaleOptions`
  - Options for the price scale this series is attached to. Separate from
    `options` because they belong to the scale, not the series.
* - `markers`
  - Markers drawn against this series.
* - `priceLines`
  - Horizontal lines drawn against this series.
* - `upDownMarkers`
  - Temporary markers showing whether a revised value rose or fell. Line and
    area series only.
* - `pane`
  - Which stacked pane to draw on, counting from 0.
```

`id` is worth dwelling on. It is not cosmetic: it is how the component matches
the series you sent last time to the one you are sending now. Keep an id stable
and the chart updates that series in place; change the id and the old series is
removed and a new one created, which resets its state. This is the same idea as
a React key or a Dash pattern-matching id.

## What a data point looks like

Two shapes, depending on the series type.

**OHLC**, for `bar` and `candlestick`:

```python
{'time': '2026-01-01', 'open': 100, 'high': 101.3, 'low': 95.1, 'close': 97.6}
```

**Single value**, for `line`, `area`, `baseline` and `histogram`:

```python
{'time': '2026-01-01', 'value': 100.35}
```

Data must be sorted by `time`, ascending, with no duplicates. The library
rejects or silently drops out-of-order points rather than sorting for you.

### Writing `time`

Three accepted spellings, and you must not mix them within one series:

```python
{'time': '2026-01-01'}                      # a date string
{'time': {'year': 2026, 'month': 1, 'day': 1}}  # the same thing, as a dict
{'time': 1767225600}                        # a UTC timestamp, in SECONDS
```

:::{warning}
Timestamps are in **seconds**, not milliseconds. Python's `time.time()` and
`datetime.timestamp()` both return seconds as a float, so `int(ts)` is what you
want. A value in milliseconds silently places your data tens of thousands of
years into the future.
:::

Whatever form you send is the form you get back. A series built from
`'2026-01-01'` strings reports `'2026-01-01'` in every crosshair and click
payload, so a callback can compare the two directly without converting.

Use timestamps when you need intraday resolution, and set
`chartOptions={'timeScale': {'timeVisible': True}}` so the axis shows the time
of day.

### Gaps

A point carrying only `time` is **whitespace**. It reserves the slot on the axis
and draws nothing:

```python
data = [
    {'time': '2026-01-01', 'value': 10},
    {'time': '2026-01-02'},               # a gap
    {'time': '2026-01-03', 'value': 12},
]
```

Do not use `None`, `float('nan')` or a missing key to mean the same thing. Only
the time-only form is understood.

### Colouring individual points

A `color` on a point overrides the series colour for that point alone. This is
how volume bars are coloured by the direction of their own candle:

```python
volume = [
    {'time': bar['time'], 'value': bar['volume'],
     'color': '#30d158' if bar['close'] >= bar['open'] else '#ff453a'}
    for bar in bars
]
```

Candlesticks also accept `borderColor` and `wickColor` per point. You do not
need a second series, and you should not use markers, to recolour bars.

## Markers

Markers are plain dictionaries in the `markers` list.

```python
{
    'id': 'price', 'type': 'line', 'data': line,
    'markers': [
        {'time': '2026-01-16', 'position': 'aboveBar', 'color': '#ff9f0a',
         'shape': 'circle', 'text': 'Signal'},
        {'time': '2026-02-01', 'position': 'belowBar', 'color': '#30d158',
         'shape': 'arrowUp', 'text': 'Buy'},
    ],
}
```

`time`, `position`, `shape` and `color` are all required. `text`, `size` and
`id` are optional.

:::{note}
A marker's `time` must match the `time` of a point that exists in the same
series. A marker on a time with no bar is dropped silently, which is the usual
reason a marker "does not appear".
:::

Markers can also be anchored to a price rather than to a bar, using
`atPriceTop`, `atPriceBottom` or `atPriceMiddle` with a `price` key. Those float
free of the data:

```python
{'time': '2026-02-01', 'position': 'atPriceTop', 'price': 118.4,
 'color': '#30d158', 'shape': 'arrowUp'}
```

## Price lines

Horizontal lines across the chart, listed on the series whose scale they are
read against.

```python
{
    'id': 'price', 'type': 'line', 'data': line,
    'priceLines': [
        {'price': 118.4, 'color': '#4a5162', 'lineStyle': 2,
         'title': 'MAX', 'axisLabelVisible': True},
    ],
}
```

The list is declarative: to remove a line, send the list without it. To move
one, send it with a different `price`.

## Panes

Panes are stacked plots sharing one horizontal axis, which is what a price chart
with volume underneath is made of. A series chooses its pane by index:

```python
dash_tvlwc.Tvlwc(
    series=[
        {'id': 'price',  'type': 'candlestick', 'data': candles, 'pane': 0},
        {'id': 'volume', 'type': 'histogram',   'data': volume,  'pane': 1},
        {'id': 'macd',   'type': 'histogram',   'data': macd,    'pane': 2},
    ],
    paneOptions=[{'stretchFactor': 3}, {'stretchFactor': 1},
                 {'stretchFactor': 1}],
)
```

Panes come into existence through `series[].pane`; an index one past the last
pane creates it. Keep the indices contiguous.

`paneOptions` is positional: the first entry sizes pane 0, and so on. Each entry
takes either `stretchFactor` (a share of the space, relative to the other panes)
or `height` (fixed pixels), but not both. Prefer `stretchFactor`, because a
fixed height does not survive a window resize.

Moving a series between panes keeps its data, options and markers. A pane whose
last series leaves is kept rather than collapsed, so the indices you chose stay
meaningful.

## Two price scales

Attach a series to the left scale and make that scale visible:

```python
dash_tvlwc.Tvlwc(
    series=[
        {'id': 'a', 'type': 'line', 'data': a,
         'options': {'priceScaleId': 'right'}},
        {'id': 'b', 'type': 'line', 'data': b,
         'options': {'priceScaleId': 'left'}},
    ],
    chartOptions={
        'leftPriceScale': {'visible': True},
        'rightPriceScale': {'visible': True},
    },
)
```

A `priceScaleId` of `''` gives the series its own hidden overlay scale, which is
the usual way to put volume behind a price without the two sharing a range.

## Where `scaleMargins` goes

`scaleMargins` is an option of the **price scale**, not of the series, which is
why it has a prop of its own. Squeezing volume into the bottom fifth of a pane
looks like this:

```python
{
    'id': 'volume', 'type': 'histogram', 'data': volume,
    'options': {'priceFormat': {'type': 'volume'}, 'priceScaleId': ''},
    'priceScaleOptions': {'scaleMargins': {'top': 0.8, 'bottom': 0}},
}
```

Putting `scaleMargins` inside `options` does nothing. This trips people up
often enough to be worth stating plainly.
