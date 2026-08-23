# What this wrapper cannot do

Some things do not survive the trip between Python and a JavaScript charting
library. This page says which, in plain terms, and what to do instead.

There is one idea behind nearly all of it:

> **A Dash prop is JSON.** It can carry numbers, strings, lists and
> dictionaries. It cannot carry a function, a class, or a piece of the page.

Everything below follows from that, plus the fact that a callback is a network
request rather than a function call.

## Anything that has to be a function

The library takes callbacks for several things: how to scale an axis, how to
parse a colour, how to format a label. None of them can be written in Python,
because there is no way to put a Python function inside a JSON prop.

**Affected:** `autoscaleInfoProvider`, `layout.colorParsers`, and every
formatter option.

**What to do instead.** Formatters have an escape hatch: write them in a small
JavaScript file in your `assets/` folder and refer to them by name. See
[Options that must be functions](options.md#options-that-must-be-functions).

For anything else, do the work in Python before the data leaves. If you want
values displayed as percentages, send percentages. If you want a custom scale,
transform the numbers and label the axis to match.

:::{note}
Versions before 0.2.0 accepted a formatter as a *string of JavaScript source*
and ran it through `eval`. That is gone. The named-function approach does the
same job without executing strings from a server response.
:::

## Plugins, custom series and drawing tools

Lightweight Charts is extensible: you can write a custom series type, or a
"primitive" that draws on the canvas, and plug it in. These are JavaScript
classes with methods the library calls while rendering.

A class cannot be a prop, and there is no partial version of this that works.

**What to do instead.** A surprising amount of what people reach for plugins for
is expressible with what is already here:

- **Bands and thresholds:** a `baseline` series, or two `line` series.
- **Annotations:** `markers` and `priceLines`.
- **Highlighting a region:** a `histogram` series with per-point colours.
- **A static trendline:** a two-point `line` series, built from the prices in
  two `click` payloads.

What genuinely is not reachable is anything that must **redraw under the cursor
during a drag**, such as a trendline you pull around with the mouse. That needs
both a plugin and sub-frame mouse handling.

## Reading the whole dataset back

There is no prop that hands you everything the chart is holding. This is a
deliberate omission rather than an oversight: a realistic series is tens of
megabytes as JSON, and every read is a network round trip.

**What to do instead.** Keep the data on the server, which is where it came
from. When you need to ask the chart something specific, `dataAction` answers
one point at a time, and `barsInLogicalRange` reports how much data surrounds
the view without sending any of it. See
[Reading data back](callbacks.md#reading-data-back).

## Anything that must happen within a frame

Every callback is a network request: roughly 10 to 50ms locally, and 100 to
300ms on a hosted app. That caps any loop that goes through Python at something
like 10 to 20 updates a second, and it is a hard floor.

For clicks, buttons and range changes this is invisible. For anything that
should track the cursor, it is not.

**What to do instead.** Use a
[clientside callback](https://dash.plotly.com/clientside-callbacks). The props
work exactly the same way; the callback simply runs in the browser instead of on
the server, so there is no round trip. Crosshair sync, a legend that follows the
cursor, and pan/zoom sync between charts are all worth writing this way.

The trade is that a clientside callback is JavaScript. It is still your Dash app,
still your props, but that particular piece of logic is no longer Python.

## Calling a method and getting an answer

Dash has no notion of calling a method on a component. Anything that is a method
in the library becomes a pair of props here: one you set to ask, one you read to
get the answer, with a callback in between.

This has two consequences worth knowing:

- **Asking twice needs a `nonce`.** A prop set to the value it already holds is
  not a change, so a repeated request needs something to differ. See
  [Commands](callbacks.md#commands-making-something-happen-once).
- **Concurrent requests cannot be told apart.** There is one result prop, so if
  you fire two queries at once you cannot be sure which answer arrived. Query
  one thing at a time.

## Coordinate conversion

The library can convert between prices and pixels. Those are pure functions, so
they cannot be props.

**What to do instead.** The mouse payloads already carry the converted values:
`price` gives the price under the cursor on each series' scale, and `logical`
gives the bar index. Between them they cover what the conversions are normally
used for.

## Custom horizontal scales

Beyond time, price and maturity, the library allows a completely custom
horizontal scale, defined by a JavaScript class. Same reason as plugins: a class
is not a prop.

The three built-in scales are available as [three components](chart_types).

## Quick reference

```{list-table}
:header-rows: 1
:widths: 34 30 36

* - You want
  - Possible?
  - Route
* - A chart option or series style
  - Yes
  - Pass it through; see [options](options)
* - A price or time formatter
  - Yes, in JavaScript
  - Named function in `assets/`
* - Formatting logic written in Python
  - No
  - Format the values before sending them
* - Custom autoscaling
  - No
  - Transform the data instead
* - A custom series type or plugin
  - No
  - Compose the built-in series types
* - A draggable drawing tool
  - No
  - A static two-point line from `click` payloads
* - A static annotation
  - Yes
  - `markers`, `priceLines`
* - Reading one data point back
  - Yes
  - `dataAction`
* - Reading the whole series back
  - No
  - Keep the data server-side
* - Reacting to a click
  - Yes
  - `subscribeClick`
* - Reacting under the cursor, instantly
  - Not from Python
  - Clientside callback
```
