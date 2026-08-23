"""The three chart components, and what differs between them.

`Tvlwc`, `Tvlwo` and `Tvlwy` are one component over three horizontal scales: a
time, a price and a maturity. They share every prop, so a callback written
against one works against the others; only what `time` means in a data point,
and which series types are accepted, differ.

Run from the repository root:

    PYTHONPATH=. python examples/chart_types.py
"""
import math

from dash import Dash, Input, Output, callback, ctx, html

import dash_tvlwc
import theme
from data_generator import generate_random_ohlc
from theme import CHART_OPTIONS, merge

# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------

PRICE = generate_random_ohlc(v0=100, n=180)

# Options chart: a payoff and an implied-volatility smile against strike. The
# horizontal position is the strike itself, so points are spaced by how far
# apart the strikes are rather than evenly.
SPOT = 100.0
STRIKES = [60, 70, 80, 85, 90, 95, 100, 105, 110, 115, 120, 130, 140, 160]

CALL_PAYOFF = [{'time': k, 'value': max(SPOT - k, 0.0)} for k in STRIKES]
SMILE = [
    {'time': k, 'value': round(18 + 0.0032 * (k - SPOT) ** 2 - 0.02 * (k - SPOT), 2)}
    for k in STRIKES
]

# Yield curve: maturities in months, which is the default `baseResolution`.
# The short end is dense and the long end is sparse, which is the whole reason
# a yield curve chart spaces points by value instead of evenly.
MATURITIES = [1, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360]


def _curve(short, long_, curvature):
    """A Nelson-Siegel-ish curve, enough to look like a real term structure."""
    out = []
    for m in MATURITIES:
        years = m / 12
        decay = (1 - math.exp(-years / 2.5)) / (years / 2.5)
        value = long_ + (short - long_) * decay + curvature * (decay - math.exp(-years / 2.5))
        out.append({'time': m, 'value': round(value, 3)})
    return out


CURVE_TODAY = _curve(short=5.35, long_=4.15, curvature=-0.9)
CURVE_YEAR_AGO = _curve(short=3.10, long_=3.95, curvature=0.4)

# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------

app = Dash(__name__, external_stylesheets=[theme.FONTS])


def readout(*pairs):
    return html.Div(className='readout', children=[
        html.Div(className='readout-row', children=[
            html.Span(k, className='readout-key'),
            html.Span(v, className='readout-value'),
        ]) for k, v in pairs
    ])


time_panel = theme.panel(
    'Tvlwc', 'createChart · horizontal axis is a time',
    dash_tvlwc.Tvlwc(
        id='time-chart', width='100%', height=260,
        chartOptions=merge(CHART_OPTIONS, {'timeScale': {'timeVisible': False}}),
        series=[{
            'id': 'px', 'type': 'candlestick', 'data': PRICE,
            'options': {'upColor': theme.GREEN, 'downColor': theme.RED,
                        'borderVisible': False,
                        'wickUpColor': theme.GREEN, 'wickDownColor': theme.RED},
        }],
        subscribeClick=True,
    ),
    html.P('Points carry `time` as a date string, a {year, month, day} dict or a '
           'UTC timestamp in seconds. All six series types are accepted.',
           className='note'),
    html.Div(id='time-readout'),
)

options_panel = theme.panel(
    'Tvlwo', 'createOptionsChart · horizontal axis is a price',
    dash_tvlwc.Tvlwo(
        id='options-chart', width='100%', height=260,
        chartOptions=merge(CHART_OPTIONS, {
            # The one option a time chart does not have: how many decimals the
            # horizontal axis labels carry.
            'localization': {'precision': 0},
        }),
        series=[
            {'id': 'payoff', 'type': 'line', 'data': CALL_PAYOFF,
             'options': {'color': theme.BLUE, 'lineWidth': 2,
                         'priceScaleId': 'right'}},
            {'id': 'smile', 'type': 'area', 'data': SMILE,
             'options': {'lineColor': theme.ORANGE,
                         'topColor': 'rgba(255, 159, 10, 0.28)',
                         'bottomColor': 'rgba(255, 159, 10, 0.02)',
                         'priceScaleId': 'left'},
             'pane': 1},
        ],
        paneOptions=[{'stretchFactor': 2}, {'stretchFactor': 1}],
        # The default view is a window of bars from the right edge, which on a
        # price axis lands nowhere near the strikes. Fitting once on load is the
        # right default for a curve, where the whole domain is the point.
        timeScaleAction={'action': 'fitContent', 'nonce': 1},
        subscribeClick=True,
    ),
    html.P('The same six series types, but `time` is the strike. Strikes are '
           'unevenly spaced and the axis honours that, so the wings sit where '
           'they belong instead of being stretched to even steps.',
           className='note'),
    html.Div(id='options-readout'),
)

yield_panel = theme.panel(
    'Tvlwy', 'createYieldCurveChart · horizontal axis is a maturity',
    dash_tvlwc.Tvlwy(
        id='yield-chart', width='100%', height=260,
        chartOptions=merge(CHART_OPTIONS, {
            'yieldCurve': {
                'baseResolution': 1,
                'minimumTimeRange': 120,
                'startTimeRange': 0,
            },
            # The maturity axis is labelled through `localization.timeFormatter`,
            # not through `yieldCurve.formatTime`: upstream declares the latter
            # but never reads it. This is a function option, so it is named
            # rather than passed, and registered in assets/tvlwc_functions.js.
            'localization': {'timeFormatter': 'maturity'},
        }),
        series=[
            {'id': 'today', 'type': 'line', 'data': CURVE_TODAY,
             'options': {'color': theme.CYAN, 'lineWidth': 2}},
            {'id': 'year-ago', 'type': 'line', 'data': CURVE_YEAR_AGO,
             'options': {'color': theme.PURPLE, 'lineWidth': 2,
                         'lineStyle': 2}},
        ],
        # Same reason as the options chart: fit the whole term structure rather
        # than opening on the last ten years, which is what `minimumTimeRange`
        # alone would give.
        timeScaleAction={'action': 'fitContent', 'nonce': 1},
        subscribeClick=True,
    ),
    html.P('`time` is a maturity in months. One month and thirty years sit at '
           'their real distance apart, which is what an evenly spaced line '
           'chart gets wrong. Line and area only: the library restricts this '
           'chart, and the component rejects the other names.',
           className='note'),
    html.Div(id='yield-readout'),
)

shared_panel = theme.panel(
    'One prop surface', 'the same callback drives all three',
    html.P('Every prop is shared, so `dataAction` is written the same way '
           'whatever the chart is. Only the answer differs, because `time` '
           'means a date, a strike and a maturity respectively.',
           className='note'),
    html.Div(id='shared-readout'),
    theme.toolbar(
        theme.button('query all three', 'shared-query'),
    ),
)

app.layout = html.Div([
    theme.topbar('chart types', 'lightweight-charts 5.2.1 · dash-tvlwc 0.2.0-dev'),
    html.Main(className='shell', children=[
        html.H1('Three horizontal scales, one component', className='page-title'),
        theme.prose(html.P(
            'The three components share a generic core. What a component adds '
            'is its constructor, the series names it accepts, and the handful '
            'of chart options its own constructor understands.'
        )),
        html.Div(className='panel-grid capability-grid', children=[
            time_panel, options_panel, yield_panel, shared_panel,
        ]),
    ]),
])


# --------------------------------------------------------------------------
# Callbacks
# --------------------------------------------------------------------------

@callback(
    Output('time-readout', 'children'),
    Input('time-chart', 'click'),
)
def time_click(payload):
    if not payload:
        return readout(('click', 'click the chart'))
    return readout(('time', str(payload['time'])),
                   ('bar index', str(payload['logical'])))


@callback(
    Output('options-readout', 'children'),
    Input('options-chart', 'click'),
)
def options_click(payload):
    if not payload:
        return readout(('click', 'click the chart'))
    # `time` here is a strike, and it comes back as the number it went in as.
    return readout(('strike', str(payload['time'])),
                   ('point index', str(payload['logical'])))


@callback(
    Output('yield-readout', 'children'),
    Input('yield-chart', 'click'),
)
def yield_click(payload):
    if not payload:
        return readout(('click', 'click the chart'))
    months = payload['time']
    label = f'{months}M' if months is None or months < 12 else f'{months / 12:g}Y'
    return readout(('maturity', f'{months} ({label})'),
                   ('point index', str(payload['logical'])))


@callback(
    Output('time-chart', 'dataAction'),
    Output('options-chart', 'dataAction'),
    Output('yield-chart', 'dataAction'),
    Input('shared-query', 'n_clicks'),
    prevent_initial_call=True,
)
def query_all(n_clicks):
    """One command shape, three charts. Only `seriesId` differs."""
    return (
        {'action': 'lastValue', 'seriesId': 'px',
         'globalLast': True, 'nonce': n_clicks},
        {'action': 'lastValue', 'seriesId': 'payoff',
         'globalLast': True, 'nonce': n_clicks},
        {'action': 'lastValue', 'seriesId': 'today',
         'globalLast': True, 'nonce': n_clicks},
    )


@callback(
    Output('shared-readout', 'children'),
    Input('time-chart', 'dataResult'),
    Input('options-chart', 'dataResult'),
    Input('yield-chart', 'dataResult'),
)
def shared_readout(time_result, options_result, yield_result):
    if not ctx.triggered_id:
        return readout(('result', 'press the button'))

    def show(result):
        if not result:
            return 'no answer yet'
        if result['noData']:
            return 'series is empty'
        return f"{result['price']:.3f}"

    return readout(('Tvlwc last close', show(time_result)),
                   ('Tvlwo last payoff', show(options_result)),
                   ('Tvlwy 30Y yield', show(yield_result)))


if __name__ == '__main__':
    app.run(debug=True, port=8052)
