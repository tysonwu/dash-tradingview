# Prop reference

Every prop of `Tvlwc`, `Tvlwo` and `Tvlwy`. The three components have an
identical prop surface; only the meaning of `time` and the accepted series types
differ, as described in [chart types](chart_types).

Nothing here is required. A component with no props renders an empty chart.

## Describing the chart

You set these. They say what the chart is.

`id`
: The Dash component id.

`series`
: List of series dictionaries. The whole of [Series and data](series).

`chartOptions`
: Chart options, passed through to the library. See [options](options).

`paneOptions`
: List, positional by pane index. Each entry takes `stretchFactor` or `height`,
  not both. Panes are created by `series[].pane`.

`watermark`
: Text or image drawn over a pane. `{'lines': [...], 'horzAlign': ...,
  'vertAlign': ...}` for text, or `{'imageUrl': ...}` for an image. `None`
  removes it. A centred text watermark needs an explicit `lineHeight` on each
  line, or it does not render.

`width`, `height`
: Size of the containing `div`. Any CSS value. Default `'100%'` and `400`.

## Turning reports on

All default to `False`, because every report is a network round trip.

`subscribeCrosshair`
: Enables `crosshair`, on every pointer move.

`subscribeClick`
: Enables `click`.

`subscribeDblClick`
: Enables `dblClick`. A double-click also fires `click`.

`subscribeVisibleRange`
: Enables `visibleRange`, `visibleLogicalRange` and `barsInLogicalRange`.

`subscribeSize`
: Enables `priceScaleWidth`, `timeScaleWidth` and `timeScaleHeight`.

`reportThrottle`
: Milliseconds to coalesce reports over, applied to every stream above. `0`, the
  default, batches to one report per animation frame.

## Commands

Set these to make something happen once. Change the `nonce` to repeat a command,
since a prop reset to the value it already holds is not a change.

`tick`
: `{'id': ..., 'bar': {...}, 'historicalUpdate': False}`, or a list of them.
  Appends a bar when its time is after the last, replaces when it matches.
  Needs no nonce, because the bar itself differs.

`timeScaleAction`
: `{'action': ..., 'nonce': ...}` where the action is `fitContent`,
  `scrollToRealTime`, `resetTimeScale` or `scrollToPosition`. The last also
  takes `position` and `animated`.

`dataAction`
: `{'action': ..., 'seriesId': ..., 'nonce': ...}` where the action is
  `dataByIndex` (with `logicalIndex`, optionally `mismatchDirection`),
  `lastValue` (optionally `globalLast`), or `pop` (with `count`). Answers on
  `dataResult`.

`crosshairPosition`
: `{'seriesId': ..., 'time': ..., 'price': ...}` places the crosshair without a
  pointer. `None` clears it. Deliberately emits no `crosshair` report, so two
  charts can drive each other.

`screenshotRequest`
: An integer. Any change captures the canvas; the PNG arrives on `screenshot`.
  `0` means no request.

## Reports

Read-only. The component writes these; use them as callback `Input`s.

`crosshair`, `click`, `dblClick`
: `{'time', 'logical', 'paneIndex', 'point', 'seriesData', 'price',
  'hoveredSeriesId', 'hoveredObjectId'}`. `seriesData` and `price` are keyed by
  your series `id`. See [the mouse payload](callbacks.md#the-mouse-payload).

`barsInLogicalRange`
: `{'barsBefore', 'barsAfter', 'from', 'to', 'seriesId'}`, describing the first
  entry in `series`. A negative `barsBefore` means the user has scrolled past
  the start of the data.

`dataResult`
: The answer to the last `dataAction`. Always carries `action` and `seriesId`,
  plus `data` for `dataByIndex`, `noData`/`price`/`color` for `lastValue`, or
  `count`/`removed` for `pop`. `removed` is newest first.

`screenshot`
: The most recent capture, as a PNG data URI.

`fullChartOptions`, `fullSeriesOptions`, `fullPriceScaleOptions`, `fullTimeScaleOptions`
: The options actually in force, defaults filled in. `fullSeriesOptions` is
  keyed by series id. Useful for checking whether an option landed.

`priceScaleWidth`, `timeScaleWidth`, `timeScaleHeight`
: Scale dimensions in pixels, for aligning something beside the chart. Behind
  `subscribeSize`.

## Two-way

Set to drive, read to follow. The component ignores a value it has just
reported, so echoing one back does not fight the user.

`visibleRange`
: `{'from': ..., 'to': ...}` in the same form your data uses. Reported only when
  `subscribeVisibleRange` is on. The library clamps a requested range to the
  data that exists, so what comes back often differs from what you set.

`visibleLogicalRange`
: `{'from': ..., 'to': ...}` in bar indices, which may be fractional and may
  fall outside the data. Setting this and `visibleRange` in one callback is
  ambiguous; this one wins.

## Series dictionary

The entries of the `series` list. Covered fully in [Series and data](series).

`id`
: **Required.** Unique within the list. Keys every payload that mentions this
  series, and decides whether an update is applied in place or the series is
  recreated.

`type`
: **Required.** `bar`, `candlestick`, `area`, `baseline`, `line`, `histogram`.
  `Tvlwy` accepts only `line` and `area`.

`data`
: **Required.** Points, ascending by `time` and unique. `{'time', 'open',
  'high', 'low', 'close'}` for OHLC types, `{'time', 'value'}` otherwise. A
  point with only `time` is whitespace and draws a gap. A `color` on a point
  overrides the series colour.

`options`
: Series styling, passed through.

`priceScaleOptions`
: Options for this series' price scale. Where `scaleMargins` belongs.

`markers`
: List of `{'time', 'position', 'shape', 'color'}`, optionally `text`, `size`,
  `id`. `time` must match a point in this series. `position` may instead be
  `atPriceTop`, `atPriceBottom` or `atPriceMiddle`, with a `price`.

`priceLines`
: List of `{'price', ...}`. Declarative: drop an entry to remove the line.

`upDownMarkers`
: `{'positiveColor', 'negativeColor', 'updateVisibilityDuration'}`, or `{}` for
  defaults. Line and area only. Marks a bar the chart already holds when a
  `tick` revises it.

`pane`
: Pane index, from 0. An index one past the last pane creates it.

## Enums

`dash_tvlwc.types` mirrors the library's enums for readability. Plain values
work identically.

```python
from dash_tvlwc.types import (
    ColorType, CrosshairMode, LastPriceAnimationMode, LineStyle, LineType,
    MismatchDirection, PriceLineSource, PriceScaleMode, SeriesType,
    TickMarkType, TrackingModeExitMode,
)
```
