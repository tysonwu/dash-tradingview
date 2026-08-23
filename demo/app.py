"""Hosted showcase for dash-tvlwc.

Every panel is the same three parts: what the capability is, a chart doing it,
and the settings that produce it. The snippets are fragments rather than
runnable files, because the point of each is the handful of keys that matter.

Run locally from the repository root:

    python demo/app.py

Hosted through `server`, the WSGI callable. On PythonAnywhere, point the web
app's WSGI file at it:

    import sys
    sys.path.insert(0, '/home/<user>/dash-tradingview')
    from demo.app import server as application

`dash_tvlwc` itself must be installed in the host's virtualenv; only the
sibling modules below are resolved by path.
"""
import copy
import os
import random
import sys
from datetime import date, timedelta

# `theme` and `data_generator` sit beside this file. Running the file directly
# puts this directory on the path, but a WSGI host imports `demo.app` from the
# repository root, where it is not. Adding it explicitly covers both, and is
# the difference between the demo starting and a bare ModuleNotFoundError.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dash import Dash, Input, Output, State, callback, ctx, dcc, html, no_update  # noqa: E402

import dash_tvlwc  # noqa: E402
import theme  # noqa: E402
from data_generator import generate_random_ohlc, generate_random_series  # noqa: E402
from theme import CHART_OPTIONS, merge  # noqa: E402

# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------

OHLC = generate_random_ohlc(v0=100, n=120)
LINE = generate_random_series(v0=100, n=120)

# Whitespace: a point carrying only `time` reserves the slot and renders as a
# gap. `None` values are not the way to do this.
GAPPED = [{'time': p['time']} if 12 < i < 20 or i > 45 else p
          for i, p in enumerate(generate_random_ohlc(v0=1, n=50, ret=0.1))]

VOLUME = generate_random_series(v0=100, n=120, ret=0.05)
for _point, _bar in zip(VOLUME, OHLC):
    # Per-point `color` overrides the series colour, so volume is coloured by
    # the direction of its own bar. No second series, no markers.
    _point['color'] = ('rgba(48, 209, 88, 0.55)' if _bar['close'] >= _bar['open']
                       else 'rgba(255, 69, 58, 0.55)')

HIST = generate_random_series(v0=100, n=50, ret=0.3)
for _i in (5, 12, 13, 14, 20, 33, 34, 46):
    HIST[_i]['color'] = theme.MINT

BASELINE = generate_random_series(v0=5000, n=60)
BASELINE_MID = sum(p['value'] for p in BASELINE) / len(BASELINE)

# Panes: a price, an oscillator and a volume, sharing one time scale.
PANE_PRICE = OHLC
PANE_MACD = [{'time': p['time'], 'value': round(p['close'] - 100, 3)}
             for p in OHLC]

# Infinite history: the whole series lives server-side and only a window of it
# is ever sent. Scrolling left past the edge asks for the next slice.
HISTORY = generate_random_ohlc(v0=100, n=1200)
HISTORY_WINDOW = 160

# Streaming seed, deliberately short so appended bars are obvious.
STREAM_SEED = generate_random_ohlc(v0=100, n=60)

# Options chart: an implied-volatility smile against strike. The horizontal
# position is the strike, so unevenly spaced strikes are spaced unevenly.
STRIKES = [60, 70, 80, 85, 90, 95, 100, 105, 110, 115, 120, 130, 140, 160]
SMILE = [{'time': k, 'value': round(18 + 0.0032 * (k - 100) ** 2 - 0.02 * (k - 100), 2)}
         for k in STRIKES]

# Yield curve: maturities in months, dense at the short end and sparse at the
# long end, which is exactly what an evenly spaced line chart draws wrong.
CURVE = [
    {'time': 1, 'value': 5.32}, {'time': 3, 'value': 5.28},
    {'time': 6, 'value': 5.11}, {'time': 12, 'value': 4.78},
    {'time': 24, 'value': 4.41}, {'time': 36, 'value': 4.25},
    {'time': 60, 'value': 4.14}, {'time': 84, 'value': 4.16},
    {'time': 120, 'value': 4.21}, {'time': 240, 'value': 4.46},
    {'time': 360, 'value': 4.39},
]

CANDLE_STYLE = {'upColor': theme.GREEN, 'downColor': theme.RED,
                'borderVisible': False,
                'wickUpColor': theme.GREEN, 'wickDownColor': theme.RED}


def chart(component_id, series, options=None, height=220, **kwargs):
    return dash_tvlwc.Tvlwc(
        id=component_id, series=series, width='100%', height=height,
        chartOptions=merge(CHART_OPTIONS, options or {}), **kwargs)


def readout(*pairs):
    return html.Div(className='readout', children=[
        html.Div(className='readout-row', children=[
            html.Span(k, className='readout-key'),
            html.Span(v, className='readout-value'),
        ]) for k, v in pairs
    ])


def next_day(iso):
    return (date.fromisoformat(iso) + timedelta(days=1)).isoformat()


# --------------------------------------------------------------------------
# Getting started
# --------------------------------------------------------------------------

minimal = theme.demo_panel(
    'Minimal example', 'series',
    chart('minimal-chart', [
        {'id': 'price', 'type': 'candlestick', 'data': OHLC[:40],
         'options': CANDLE_STYLE},
        {'id': 'signal', 'type': 'line', 'data': LINE[:40],
         'options': {'color': theme.CYAN, 'lineWidth': 2}},
    ]),
    """
    import dash_tvlwc

    dash_tvlwc.Tvlwc(
        # Every series carries its own id, type and data. The id is what keys
        # the crosshair, click and read-back payloads later on.
        series=[
            {'id': 'price', 'type': 'candlestick', 'data': candlestick_data},
            {'id': 'signal', 'type': 'line', 'data': line_data},
        ],
    )
    """,
)

streaming = theme.demo_panel(
    'Live streaming', 'tick',
    html.Div(className='hero', children=[
        html.Div(className='hero-readout', children=[
            html.Span(id='stream-price', className='hero-price'),
            html.Span(id='stream-date', className='hero-date'),
        ]),
        chart('stream-chart', [
            {'id': 'px', 'type': 'candlestick', 'data': STREAM_SEED,
             'options': CANDLE_STYLE},
        ], height=300, subscribeCrosshair=True, reportThrottle=50),
    ]),
    """
    # `tick` appends one bar without resending the series, so the visible range
    # does not move and the payload stays the size of a single bar. Rewriting
    # `series` on a timer sends the whole history on every update instead.
    @callback(Output('chart', 'tick'), Input('timer', 'n_intervals'), ...)
    def stream(n):
        return {'id': 'px', 'bar': next_bar}

    # A bar whose time matches the last one replaces it, so a live candle can
    # be revised in place. `historicalUpdate=True` amends an older bar.
    """,
    theme.toolbar(
        theme.button('Start / stop', 'stream-toggle'),
        theme.button('Revise last bar', 'stream-revise'),
    ),
)

# --------------------------------------------------------------------------
# Series types
# --------------------------------------------------------------------------

bar_panel = theme.demo_panel(
    'Bar', "type = 'bar'",
    chart('bar-chart', [{'id': 'px', 'type': 'bar', 'data': OHLC[:50],
                         'options': {'upColor': theme.GREEN,
                                     'downColor': theme.RED,
                                     'thinBars': False}}]),
    """
    series=[{
        'id': 'px', 'type': 'bar', 'data': ohlc,
        'options': {'upColor': '#30d158', 'downColor': '#ff453a',
                    'thinBars': False},
    }]
    """,
)

candlestick_panel = theme.demo_panel(
    'Candlestick', 'whitespace points become gaps',
    chart('candlestick-chart', [{
        'id': 'px', 'type': 'candlestick', 'data': GAPPED,
        'options': {'upColor': theme.ORANGE, 'downColor': theme.PURPLE,
                    'borderVisible': False,
                    'wickUpColor': theme.ORANGE,
                    'wickDownColor': theme.PURPLE},
    }]),
    """
    # A point carrying only `time` is whitespace: it holds the slot and draws
    # nothing. Use it for gaps rather than a None value.
    data = [
        {'time': '2026-01-01', 'open': 1, 'high': 2, 'low': 0.5, 'close': 1.5},
        {'time': '2026-01-02'},
        {'time': '2026-01-03', 'open': 1.5, 'high': 2, 'low': 1, 'close': 1.8},
    ]
    """,
)

area_panel = theme.demo_panel(
    'Area', 'localization.priceFormatter',
    chart('area-chart', [{
        'id': 'px', 'type': 'area', 'data': generate_random_series(v0=15, n=50),
        'options': {'lineColor': theme.BLUE, 'lineWidth': 2,
                    'topColor': 'rgba(10, 132, 255, 0.35)',
                    'bottomColor': 'rgba(10, 132, 255, 0.02)',
                    'priceLineColor': theme.BORDER},
    }], {'localization': {'priceFormatter': 'usd'}}),
    """
    # An option that must be a JavaScript function cannot cross a JSON prop
    # boundary, so it is named instead. Register the name in an assets file:
    #
    #   window.dashTvlwcFunctions = window.dashTvlwcFunctions || {};
    #   window.dashTvlwcFunctions.usd = (p) => '$' + p.toFixed(2);
    chartOptions={'localization': {'priceFormatter': 'usd'}}
    """,
)

baseline_panel = theme.demo_panel(
    'Baseline', 'priceLines, left price scale',
    chart('baseline-chart', [{
        'id': 'px', 'type': 'baseline', 'data': BASELINE,
        'options': {
            'baseValue': {'type': 'price', 'price': BASELINE_MID},
            'topLineColor': theme.GREEN,
            'topFillColor1': 'rgba(48, 209, 88, 0.28)',
            'topFillColor2': 'rgba(48, 209, 88, 0.02)',
            'bottomLineColor': theme.RED,
            'bottomFillColor1': 'rgba(255, 69, 58, 0.02)',
            'bottomFillColor2': 'rgba(255, 69, 58, 0.28)',
            'lineWidth': 2, 'priceScaleId': 'left',
        },
        'priceLines': [{'price': max(p['value'] for p in BASELINE),
                        'color': theme.BORDER, 'lineStyle': 2,
                        'title': 'MAX', 'axisLabelVisible': True}],
    }], {'rightPriceScale': {'visible': False},
         'leftPriceScale': {'visible': True, 'borderColor': theme.BORDER}}),
    """
    series=[{
        'id': 'px', 'type': 'baseline', 'data': values,
        'options': {
            'baseValue': {'type': 'price', 'price': mid},
            'priceScaleId': 'left',
        },
        # Price lines are declarative, and removing one is a matter of
        # dropping it from this list.
        'priceLines': [{'price': high, 'title': 'MAX',
                        'lineStyle': 2, 'axisLabelVisible': True}],
    }]

    chartOptions={'leftPriceScale': {'visible': True},
                  'rightPriceScale': {'visible': False}}
    """,
)

volume_panel = theme.demo_panel(
    'Line and volume', 'priceScaleOptions.scaleMargins',
    chart('volume-chart', [
        {'id': 'px', 'type': 'line', 'data': LINE,
         'options': {'lineWidth': 2, 'color': theme.CYAN}},
        {'id': 'vol', 'type': 'histogram', 'data': VOLUME,
         'options': {'priceFormat': {'type': 'volume'}, 'priceScaleId': '',
                     'priceLineVisible': False, 'lastValueVisible': False},
         'priceScaleOptions': {'scaleMargins': {'top': 0.82, 'bottom': 0}}},
    ]),
    """
    {
        'id': 'vol', 'type': 'histogram', 'data': volume,
        # An empty priceScaleId gives the series its own hidden overlay scale.
        'options': {'priceFormat': {'type': 'volume'}, 'priceScaleId': ''},
        # `scaleMargins` belongs to the price scale, not to the series, which
        # is why it has a prop of its own. Squeezing the volume into the
        # bottom fifth is what keeps it out of the price.
        'priceScaleOptions': {'scaleMargins': {'top': 0.82, 'bottom': 0}},
    }
    """,
)

histogram_panel = theme.demo_panel(
    'Histogram', 'per-point color, base',
    chart('histogram-chart', [{
        'id': 'value', 'type': 'histogram', 'data': HIST,
        'options': {'color': theme.PURPLE, 'base': 100,
                    'priceLineVisible': False, 'lastValueVisible': False},
    }]),
    """
    # A `color` on the point overrides the series colour, so bars can be
    # classified without a second series.
    data = [{'time': '2026-01-01', 'value': 120, 'color': '#63e6e2'}, ...]

    'options': {'color': '#bf5af2', 'base': 100}
    """,
)

# --------------------------------------------------------------------------
# Capabilities
# --------------------------------------------------------------------------

panes_panel = theme.demo_panel(
    'Panes', 'series[].pane, paneOptions',
    chart('panes-chart', [
        {'id': 'px', 'type': 'candlestick', 'data': PANE_PRICE,
         'options': CANDLE_STYLE, 'pane': 0},
        {'id': 'macd', 'type': 'histogram', 'data': PANE_MACD,
         'options': {'color': theme.INDIGO, 'priceLineVisible': False},
         'pane': 1},
        {'id': 'vol', 'type': 'histogram', 'data': VOLUME,
         'options': {'priceFormat': {'type': 'volume'},
                     'priceLineVisible': False, 'lastValueVisible': False},
         'pane': 2},
    ], height=420),
    """
    # Panes stack vertically and share one time scale: the shared-x-axis
    # subplot, without a second chart to keep in sync. A pane index one past
    # the last pane creates it.
    series=[
        {'id': 'px',   'type': 'candlestick', 'data': ohlc,   'pane': 0},
        {'id': 'macd', 'type': 'histogram',   'data': macd,   'pane': 1},
        {'id': 'vol',  'type': 'histogram',   'data': volume, 'pane': 2},
    ],
    # Positional by pane index. Prefer stretchFactor to a fixed height, which
    # does not survive a window resize.
    paneOptions=[{'stretchFactor': 3}, {'stretchFactor': 1},
                 {'stretchFactor': 1}],
    """,
    theme.toolbar(
        theme.button('3:1:1', 'panes-even'),
        theme.button('6:1:1', 'panes-tall'),
    ),
)

updown_panel = theme.demo_panel(
    'Revision markers', 'series[].upDownMarkers',
    chart('updown-chart', [{
        'id': 'px', 'type': 'line', 'data': LINE[:60],
        'options': {'color': theme.BLUE, 'lineWidth': 2},
        'upDownMarkers': {'positiveColor': theme.GREEN,
                          'negativeColor': theme.RED,
                          'updateVisibilityDuration': 4000},
    }]),
    """
    # A temporary marker coloured by whether a revised value rose or fell.
    # It appears when a `tick` revises a bar the chart already holds, which is
    # what a late correction on a live feed looks like.
    series=[{
        'id': 'px', 'type': 'line', 'data': values,
        'upDownMarkers': {'positiveColor': '#30d158',
                          'negativeColor': '#ff453a',
                          'updateVisibilityDuration': 4000},
    }]
    """,
    theme.toolbar(
        theme.button('Revise up', 'updown-up'),
        theme.button('Revise down', 'updown-down'),
    ),
)

markers_panel = theme.demo_panel(
    'Markers', 'series[].markers',
    chart('markers-chart', [{
        'id': 'px', 'type': 'line', 'data': LINE[:60],
        'options': {'color': theme.MINT, 'lineWidth': 2},
        'markers': [
            {'time': LINE[15]['time'], 'position': 'aboveBar',
             'color': theme.ORANGE, 'shape': 'circle', 'text': 'Signal'},
            {'time': LINE[30]['time'], 'position': 'belowBar',
             'color': theme.GREEN, 'shape': 'arrowUp', 'text': 'Buy'},
            {'time': LINE[45]['time'], 'position': 'aboveBar',
             'color': theme.RED, 'shape': 'arrowDown', 'text': 'Sell'},
        ],
    }]),
    """
    'markers': [
        # Anchored to a bar. `time` must match a point in this series' data
        # or the marker is dropped without a word.
        {'time': '2026-01-16', 'position': 'aboveBar',
         'color': '#ff9f0a', 'shape': 'circle', 'text': 'Signal'},
        # Anchored to a price instead, which floats free of the bars.
        {'time': '2026-02-01', 'position': 'atPriceTop',
         'price': 118.4, 'color': '#30d158', 'shape': 'arrowUp'},
    ]
    """,
)

annotate_panel = theme.demo_panel(
    'Click to annotate', 'subscribeClick, click',
    chart('annotate-chart', [{
        'id': 'px', 'type': 'line', 'data': LINE[:80],
        'options': {'color': theme.YELLOW, 'lineWidth': 2},
    }], subscribeClick=True),
    """
    # The click payload carries the price under the cursor on each series'
    # own scale, so a price line can be drawn where the user clicked without
    # exposing the coordinate conversions as props.
    dash_tvlwc.Tvlwc(id='chart', series=..., subscribeClick=True)

    @callback(Output('chart', 'series'), Input('chart', 'click'), ...)
    def annotate(click, series):
        price = click['price']['px']
        series[0]['priceLines'] = [{'price': price, 'title': 'clicked',
                                    'axisLabelVisible': True}]
        return series
    """,
    theme.toolbar(theme.button('Clear', 'annotate-clear')),
    html.Div(id='annotate-readout'),
)

history_panel = theme.demo_panel(
    'Infinite history', 'barsInLogicalRange',
    chart('history-chart', [{
        'id': 'px', 'type': 'candlestick', 'data': HISTORY[-HISTORY_WINDOW:],
        'options': CANDLE_STYLE,
    }], subscribeVisibleRange=True, reportThrottle=120),
    """
    # `barsInLogicalRange` reports how much data lies either side of the view,
    # as a fixed-size payload rather than the data itself. A negative
    # barsBefore means the user has scrolled past the start: fetch more.
    dash_tvlwc.Tvlwc(id='chart', series=..., subscribeVisibleRange=True)

    @callback(Output('chart', 'series'),
              Input('chart', 'barsInLogicalRange'), ...)
    def page(bars, loaded):
        if bars['barsBefore'] > 20:
            raise PreventUpdate
        return [{'id': 'px', 'type': 'candlestick',
                 'data': history[-(loaded + 160):]}]
    """,
    html.Div(id='history-readout'),
)

query_panel = theme.demo_panel(
    'Read the data back', 'dataAction, dataResult',
    chart('query-chart', [{
        'id': 'px', 'type': 'line', 'data': LINE[:60],
        'options': {'color': theme.PURPLE, 'lineWidth': 2},
    }]),
    """
    # Dash cannot call a method and take its return value, so a query is a
    # command prop in and a result prop out. Every answer here is O(1), so
    # none of them ships the dataset back over the wire.
    dataAction={'action': 'dataByIndex', 'seriesId': 'px',
                'logicalIndex': 0, 'nonce': n_clicks}
    # -> dataResult {'action': ..., 'data': {'time': ..., 'value': ...}}

    {'action': 'lastValue', 'seriesId': 'px', 'globalLast': True}
    # -> {'noData': False, 'price': 105.5, 'color': '#bf5af2'}

    # `pop` is the counterpart to `tick`: trim the end without resending.
    {'action': 'pop', 'seriesId': 'px', 'count': 5}
    """,
    theme.toolbar(
        theme.button('First bar', 'query-first'),
        theme.button('Last value', 'query-last'),
        theme.button('Pop 5', 'query-pop'),
        theme.button('Reset', 'query-reset'),
    ),
    html.Div(id='query-readout'),
)

watermark_panel = theme.demo_panel(
    'Watermark', 'watermark',
    chart('watermark-chart', [{
        'id': 'px', 'type': 'area', 'data': LINE[:60],
        'options': {'lineColor': theme.TEAL, 'lineWidth': 2,
                    'topColor': 'rgba(64, 203, 224, 0.3)',
                    'bottomColor': 'rgba(64, 203, 224, 0.02)'},
    }], watermark={
        'lines': [{'text': 'DASH-TVLWC', 'color': 'rgba(238, 240, 247, 0.16)',
                   'fontSize': 34, 'lineHeight': 40}],
        'horzAlign': 'center', 'vertAlign': 'center',
    }),
    """
    watermark={
        'lines': [{'text': 'DASH-TVLWC', 'fontSize': 34,
                   'color': 'rgba(238, 240, 247, 0.16)',
                   # Centring computes a text height from lineHeight, and the
                   # defaults do not supply one, so a centred watermark
                   # without it never appears.
                   'lineHeight': 40}],
        'horzAlign': 'center', 'vertAlign': 'center',
    }
    # Give `imageUrl` instead of `lines` for an image watermark.
    """,
    theme.toolbar(
        theme.button('Text', 'wm-text'),
        theme.button('Corner', 'wm-corner'),
        theme.button('None', 'wm-none'),
    ),
)

screenshot_panel = theme.demo_panel(
    'Screenshot', 'screenshotRequest, screenshot',
    chart('shot-chart', [{
        'id': 'px', 'type': 'candlestick', 'data': OHLC[:60],
        'options': CANDLE_STYLE,
    }]),
    """
    # Increment the request; the PNG arrives as a data URI on `screenshot`.
    dash_tvlwc.Tvlwc(id='chart', screenshotRequest=n_clicks)

    @callback(Output('shot', 'src'), Input('chart', 'screenshot'))
    def show(data_uri):
        return data_uri
    """,
    theme.toolbar(theme.button('Capture', 'shot-take')),
    html.Div(id='shot-out'),
)

sync_panel = html.Div(className='wide', children=[theme.demo_panel(
    'Crosshair sync', 'crosshair in, crosshairPosition out',
    html.Div(className='chart-pair', children=[
        chart('sync-a', [{'id': 'px', 'type': 'line', 'data': LINE,
                          'options': {'color': theme.CYAN, 'lineWidth': 2}}],
              subscribeCrosshair=True, reportThrottle=0, height=200),
        chart('sync-b', [{'id': 'px', 'type': 'line',
                          'data': [{'time': p['time'],
                                    'value': p['value'] * 0.85 + 12}
                                   for p in LINE],
                          'options': {'color': theme.ORANGE, 'lineWidth': 2}}],
              subscribeCrosshair=True, reportThrottle=0, height=200),
    ]),
    """
    # Hover either chart and the other follows. Placing the crosshair from
    # Python routes through a synthetic position that skips the crosshair
    # event, so two charts pointed at each other cannot feed back, and Dash
    # keys on component plus property, so this is not a callback cycle.
    @callback(Output('b', 'crosshairPosition'),
              Output('a', 'crosshairPosition'),
              Input('a', 'crosshair'), Input('b', 'crosshair'))
    def sync(a, b):
        source = a if ctx.triggered_id == 'a' else b
        target = {'seriesId': 'px', 'time': source['time'],
                  'price': source['price']['px']}
        return (target, no_update) if ctx.triggered_id == 'a' \\
            else (no_update, target)
    """,
)])

# --------------------------------------------------------------------------
# Other chart types
# --------------------------------------------------------------------------

options_chart_panel = theme.demo_panel(
    'Tvlwo', 'createOptionsChart, horizontal axis is a price',
    dash_tvlwc.Tvlwo(
        id='smile-chart', width='100%', height=220,
        chartOptions=merge(CHART_OPTIONS, {'localization': {'precision': 0}}),
        series=[{'id': 'iv', 'type': 'area', 'data': SMILE,
                 'options': {'lineColor': theme.ORANGE, 'lineWidth': 2,
                             'topColor': 'rgba(255, 159, 10, 0.28)',
                             'bottomColor': 'rgba(255, 159, 10, 0.02)'}}],
        timeScaleAction={'action': 'fitContent', 'nonce': 1},
    ),
    """
    # Same props as Tvlwc, but `time` is a position on a price axis. Strikes
    # sit at their real distance apart rather than at even steps.
    dash_tvlwc.Tvlwo(
        series=[{'id': 'iv', 'type': 'area', 'data': [
            {'time': 60, 'value': 25.1}, {'time': 100, 'value': 18.0},
            {'time': 160, 'value': 24.3},
        ]}],
        # How many decimals the axis labels carry.
        chartOptions={'localization': {'precision': 0}},
    )
    """,
)

yield_chart_panel = theme.demo_panel(
    'Tvlwy', 'createYieldCurveChart, horizontal axis is a maturity',
    dash_tvlwc.Tvlwy(
        id='curve-chart', width='100%', height=220,
        chartOptions=merge(CHART_OPTIONS, {
            'yieldCurve': {'baseResolution': 1, 'minimumTimeRange': 120,
                           'startTimeRange': 0},
            'localization': {'timeFormatter': 'maturity'},
        }),
        series=[{'id': 'curve', 'type': 'line', 'data': CURVE,
                 'options': {'color': theme.CYAN, 'lineWidth': 2}}],
        timeScaleAction={'action': 'fitContent', 'nonce': 1},
    ),
    """
    # `time` is a maturity in months, so one month and thirty years sit at
    # their real distance apart. Line and area series only.
    dash_tvlwc.Tvlwy(
        series=[{'id': 'curve', 'type': 'line', 'data': [
            {'time': 1, 'value': 5.32}, {'time': 120, 'value': 4.21},
            {'time': 360, 'value': 4.39},
        ]}],
        chartOptions={
            'yieldCurve': {'baseResolution': 1, 'minimumTimeRange': 120},
            # The maturity axis formats through `localization.timeFormatter`,
            # named like any other function option.
            'localization': {'timeFormatter': 'maturity'},
        },
    )
    """,
)

# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------

app = Dash(__name__, external_stylesheets=[theme.FONTS],
           title='dash-tvlwc')
# The WSGI callable. A host such as PythonAnywhere imports this, and never
# runs the `__main__` block below.
server = app.server

app.layout = html.Div([
    # Off until asked for. An idle demo should not be spending a request a
    # second on a shared host.
    dcc.Interval(id='timer', interval=900, disabled=True),
    dcc.Store(id='stream-state', data={'time': STREAM_SEED[-1]['time'],
                                       'close': STREAM_SEED[-1]['close']}),
    dcc.Store(id='history-loaded', data=HISTORY_WINDOW),

    theme.topbar('dash-tvlwc', 'lightweight-charts 5.2.1 · dash-tvlwc 0.2.0'),
    html.Main(className='shell', children=[
        html.H1('Tradingview Lightweight Charts for Dash',
                className='page-title'),
        theme.prose(dcc.Markdown('''
        A [Dash](https://dash.plotly.com/) component wrapping
        [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts),
        driven entirely from Python callbacks. Source on
        [Github](https://github.com/tysonwu/dash-tradingview), released on
        [PyPI](https://pypi.org/project/dash-tvlwc/).

        Every panel below shows the settings that produce it.
        ''', link_target='_blank')),

        html.H2('Getting started', className='section-title'),
        html.Div(className='panel-grid demo-grid',
                 children=[minimal, streaming]),

        html.H2('Series types', className='section-title'),
        html.Div(className='panel-grid demo-grid', children=[
            bar_panel, candlestick_panel, area_panel,
            baseline_panel, volume_panel, histogram_panel,
        ]),

        html.H2('Reading and driving the chart', className='section-title'),
        html.Div(className='panel-grid demo-grid', children=[
            panes_panel, updown_panel, markers_panel, annotate_panel,
            history_panel, query_panel, watermark_panel, screenshot_panel,
            sync_panel,
        ]),

        html.H2('Other chart types', className='section-title'),
        html.Div(className='panel-grid demo-grid',
                 children=[options_chart_panel, yield_chart_panel]),

        html.Div(className='footer', children=[
            html.Span('By Tyson Wu'),
            html.Span('MIT licensed · charts by TradingView'),
        ]),
    ]),
])


# --------------------------------------------------------------------------
# Callbacks
# --------------------------------------------------------------------------

@callback(
    Output('timer', 'disabled'),
    Input('stream-toggle', 'n_clicks'),
    State('timer', 'disabled'),
    prevent_initial_call=True,
)
def toggle_stream(n_clicks, disabled):
    return not disabled


@callback(
    Output('stream-chart', 'tick'),
    Output('stream-state', 'data'),
    Input('timer', 'n_intervals'),
    Input('stream-revise', 'n_clicks'),
    State('stream-state', 'data'),
    prevent_initial_call=True,
)
def stream(n_intervals, revise, state):
    if ctx.triggered_id == 'stream-revise':
        # A bar whose time matches the last one replaces it rather than
        # appending, which is how a live candle is revised in place.
        bar = generate_random_ohlc(v0=state['close'], n=1, t0=state['time'])[0]
        return {'id': 'px', 'bar': bar}, state

    when = next_day(state['time'])
    bar = generate_random_ohlc(v0=state['close'], n=1, t0=when)[0]
    return ({'id': 'px', 'bar': bar},
            {'time': when, 'close': bar['close']})


@callback(
    Output('stream-date', 'children'),
    Output('stream-price', 'children'),
    Input('stream-chart', 'crosshair'),
)
def stream_readout(crosshair):
    # `seriesData` is keyed by the id given in `series`, and holds the whole
    # data point rather than a bare price.
    point = (crosshair or {}).get('seriesData', {}).get('px')
    time = (crosshair or {}).get('time')
    if not point or not time:
        return 'Hover for date and price', ''
    return time, f"${point.get('close', point.get('value')):,.2f}"


@callback(
    Output('panes-chart', 'paneOptions'),
    Input('panes-even', 'n_clicks'),
    Input('panes-tall', 'n_clicks'),
    prevent_initial_call=True,
)
def pane_sizes(even, tall):
    if ctx.triggered_id == 'panes-even':
        return [{'stretchFactor': 3}, {'stretchFactor': 1}, {'stretchFactor': 1}]
    return [{'stretchFactor': 6}, {'stretchFactor': 1}, {'stretchFactor': 1}]


@callback(
    Output('updown-chart', 'tick'),
    Input('updown-up', 'n_clicks'),
    Input('updown-down', 'n_clicks'),
    State('updown-chart', 'series'),
    prevent_initial_call=True,
)
def revise(up, down, series):
    # The plugin only marks a revision of a bar it already holds, so this
    # rewrites an existing point rather than appending a new one.
    point = series[0]['data'][-3]
    factor = 1.05 if ctx.triggered_id == 'updown-up' else 0.95
    return {'id': 'px',
            'bar': {'time': point['time'],
                    'value': round(point['value'] * factor, 3)},
            'historicalUpdate': True}


@callback(
    Output('annotate-chart', 'series'),
    Output('annotate-readout', 'children'),
    Input('annotate-chart', 'click'),
    Input('annotate-clear', 'n_clicks'),
    State('annotate-chart', 'series'),
    prevent_initial_call=True,
)
def annotate(click, clear, series):
    series = copy.deepcopy(series)
    if ctx.triggered_id == 'annotate-clear' or not click:
        series[0]['priceLines'] = []
        return series, readout(('click', 'click the chart'))

    price = (click.get('price') or {}).get('px')
    if price is None:
        return no_update, no_update
    series[0]['priceLines'] = [{'price': price, 'color': theme.ORANGE,
                                'lineStyle': 2, 'title': 'clicked',
                                'axisLabelVisible': True}]
    return series, readout(('time', str(click.get('time'))),
                           ('price', f'{price:,.2f}'))


@callback(
    Output('history-chart', 'series'),
    Output('history-loaded', 'data'),
    Output('history-readout', 'children'),
    Input('history-chart', 'barsInLogicalRange'),
    State('history-loaded', 'data'),
    prevent_initial_call=True,
)
def page_history(bars, loaded):
    if not bars:
        return no_update, no_update, no_update
    before = bars.get('barsBefore')
    text = readout(('barsBefore', f'{before:.0f}' if before is not None else '-'),
                   ('loaded', f'{loaded} of {len(HISTORY)}'))
    if before is None or before > 20 or loaded >= len(HISTORY):
        return no_update, no_update, text

    loaded = min(loaded + HISTORY_WINDOW, len(HISTORY))
    series = [{'id': 'px', 'type': 'candlestick',
               'data': HISTORY[-loaded:], 'options': CANDLE_STYLE}]
    return series, loaded, readout(('barsBefore', f'{before:.0f}'),
                                   ('loaded', f'{loaded} of {len(HISTORY)}'))


@callback(
    Output('query-chart', 'dataAction'),
    Output('query-chart', 'series'),
    Input('query-first', 'n_clicks'),
    Input('query-last', 'n_clicks'),
    Input('query-pop', 'n_clicks'),
    Input('query-reset', 'n_clicks'),
    State('query-chart', 'series'),
    prevent_initial_call=True,
)
def query(first, last, pop, reset, series):
    which = ctx.triggered_id
    if which == 'query-reset':
        # `pop` mutated the chart without touching the prop, so rewriting
        # `series` is what puts the two back in agreement.
        series = copy.deepcopy(series)
        series[0]['data'] = LINE[:60]
        return no_update, series
    if which == 'query-first':
        action = {'action': 'dataByIndex', 'seriesId': 'px',
                  'logicalIndex': 0, 'nonce': first}
    elif which == 'query-last':
        action = {'action': 'lastValue', 'seriesId': 'px',
                  'globalLast': True, 'nonce': last}
    else:
        action = {'action': 'pop', 'seriesId': 'px', 'count': 5, 'nonce': pop}
    return action, no_update


@callback(
    Output('query-readout', 'children'),
    Input('query-chart', 'dataResult'),
)
def query_readout(result):
    if not result:
        return readout(('result', 'press a button'))
    action = result['action']
    if action == 'dataByIndex':
        point = result['data']
        return readout(('action', action),
                       ('data', 'None' if point is None
                        else f"{point['time']} · {point['value']:.2f}"))
    if action == 'lastValue':
        if result['noData']:
            return readout(('action', action), ('value', 'series is empty'))
        return readout(('action', action), ('price', f"{result['price']:.2f}"),
                       ('color', result['color']))
    removed = result['removed']
    return readout(('action', action),
                   ('removed', f"{len(removed)} bars, newest "
                               f"{removed[0]['time']}" if removed else 'none'))


@callback(
    Output('watermark-chart', 'watermark'),
    Input('wm-text', 'n_clicks'),
    Input('wm-corner', 'n_clicks'),
    Input('wm-none', 'n_clicks'),
    prevent_initial_call=True,
)
def watermark(text, corner, none):
    if ctx.triggered_id == 'wm-none':
        return None
    if ctx.triggered_id == 'wm-corner':
        return {'lines': [{'text': 'dash-tvlwc', 'color': theme.MUTED_FOREGROUND,
                           'fontSize': 13, 'lineHeight': 18}],
                'horzAlign': 'left', 'vertAlign': 'top'}
    return {'lines': [{'text': 'DASH-TVLWC',
                       'color': 'rgba(238, 240, 247, 0.16)',
                       'fontSize': 34, 'lineHeight': 40}],
            'horzAlign': 'center', 'vertAlign': 'center'}


@callback(
    Output('shot-chart', 'screenshotRequest'),
    Input('shot-take', 'n_clicks'),
    prevent_initial_call=True,
)
def request_shot(n_clicks):
    return n_clicks


@callback(
    Output('shot-out', 'children'),
    Input('shot-chart', 'screenshot'),
    prevent_initial_call=True,
)
def show_shot(data_uri):
    if not data_uri:
        return no_update
    return html.Img(src=data_uri,
                    style={'width': '100%', 'marginTop': '8px',
                           'border': f'1px solid {theme.BORDER}'})


@callback(
    Output('sync-b', 'crosshairPosition'),
    Output('sync-a', 'crosshairPosition'),
    Input('sync-a', 'crosshair'),
    Input('sync-b', 'crosshair'),
    prevent_initial_call=True,
)
def sync_crosshair(a, b):
    # Whichever chart the pointer is over drives the other. Dash keys on
    # component plus property, so a pair of these is not a cycle.
    source = a if ctx.triggered_id == 'sync-a' else b
    if not source or source.get('time') is None:
        return None, None
    price = (source.get('price') or {}).get('px')
    if price is None:
        return no_update, no_update
    target = {'seriesId': 'px', 'time': source['time'], 'price': price}
    if ctx.triggered_id == 'sync-a':
        return target, no_update
    return no_update, target


if __name__ == '__main__':
    app.run(debug=True)
