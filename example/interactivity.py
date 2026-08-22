"""Driving the chart from Dash callbacks.

Run from the repository root:

    python example/interactivity.py

Everything about a series now lives in one `series` prop, so callbacks that used
to write `seriesData`, `seriesTypes`, `seriesMarkers` and friends separately have
to become a single callback that inspects `ctx.triggered_id`. Two callbacks
cannot write the same prop without `allow_duplicate=True`.
"""
import copy
import random
from datetime import date, timedelta

from dash import Dash, Input, Output, State, callback, ctx, html

import dash_tvlwc
import theme
from data_generator import generate_random_ohlc, generate_random_series
from theme import CHART_OPTIONS, merge

# Named function registered in assets/tvlwc_functions.js.
CHARTS = merge(CHART_OPTIONS, {'localization': {'priceFormatter': 'usd'}})

# Two console layers, so the toggle stays inside the palette rather than
# introducing a decorative colour.
BACKGROUNDS = [theme.CARD, theme.ACCENT]

CANDLES = generate_random_ohlc(v0=100, n=50)
AREA = generate_random_series(v0=15, n=50)
LINE = generate_random_series(v0=15, n=50)

CHART_2_SERIES = [
    {
        'id': 'area',
        'type': 'area',
        'data': AREA,
        'options': {
            'lineColor': theme.TEAL,
            'topColor': 'rgba(64, 203, 224, 0.30)',
            'bottomColor': 'rgba(64, 203, 224, 0.02)',
            'priceLineWidth': 2,
        },
        # Marker colour is semantic: entry against exit.
        'markers': [
            {'time': AREA[15]['time'], 'position': 'belowBar',
             'color': theme.GREEN, 'shape': 'arrowUp', 'text': 'Buy'},
            {'time': AREA[20]['time'], 'position': 'aboveBar',
             'color': theme.RED, 'shape': 'arrowDown', 'text': 'Sell'},
        ],
        'priceLines': [
            {'price': 15, 'color': theme.BORDER, 'lineStyle': 2,
             'title': 'LEVEL', 'axisLabelVisible': True},
        ],
    },
    {
        'id': 'line',
        'type': 'line',
        'data': LINE,
        'options': {'priceLineWidth': 1, 'color': theme.BLUE},
    },
]


def switch_between(current, options):
    return random.choice([opt for opt in options if opt != current])


panel1 = theme.panel(
    'Chart 1', 'series + chartOptions',
    dash_tvlwc.Tvlwc(
        id='chart-1',
        series=[{'id': 'price', 'type': 'candlestick', 'data': CANDLES,
                 'options': {'upColor': theme.GREEN, 'downColor': theme.RED,
                             'borderVisible': False,
                             'wickUpColor': theme.GREEN,
                             'wickDownColor': theme.RED}}],
        width='100%',
        height=260,
        chartOptions=CHARTS,
        # Reporting the crosshair costs a server round trip per report, so it is
        # off unless asked for. `reportThrottle` coalesces reports; zero
        # batches to one per animation frame.
        subscribeCrosshair=True,
        subscribeClick=True,
        subscribeVisibleRange=True,
        reportThrottle=100,
    ),
    theme.toolbar(
        theme.button('Switch type', 'switch-type'),
        theme.button('Append bar', 'append-bar'),
        theme.button('Switch layer', 'switch-background'),
    ),
)

panel2 = theme.panel(
    'Chart 2', 'markers, price lines, options',
    dash_tvlwc.Tvlwc(
        id='chart-2',
        series=CHART_2_SERIES,
        width='100%',
        height=260,
        chartOptions=CHARTS,
    ),
    theme.toolbar(
        theme.button('Move price line', 'move-price-line'),
        theme.button('Move markers', 'move-markers'),
        theme.button('Recolour line', 'recolour-line'),
    ),
)

panel3 = theme.panel(
    'Chart 1 events', 'crosshair · click · visibleLogicalRange',
    html.Div(id='readout', className='readout'),
    theme.toolbar(theme.button('Add a chart', 'add-chart')),
    html.Div(id='extra-chart', style={'marginTop': '8px'}),
)

app = Dash(__name__, external_stylesheets=[theme.FONTS])
app.layout = html.Div([
    theme.topbar('Callback interactivity',
                 'lightweight-charts 5.2.1 · dash-tvlwc 0.2.0-dev'),
    html.Main(className='shell', children=[
        html.Div(className='panel-grid interactivity-grid',
                 children=[panel1, panel2, panel3]),
    ]),
])


@callback(
    Output('chart-1', 'series'),
    Input('switch-type', 'n_clicks'),
    Input('append-bar', 'n_clicks'),
    State('chart-1', 'series'),
    prevent_initial_call=True,
)
def update_chart_1(switch_clicks, append_clicks, series):
    """One callback for every button that writes `series`."""
    series = copy.deepcopy(series)
    price = series[0]

    if ctx.triggered_id == 'switch-type':
        price['type'] = switch_between(price['type'], ['bar', 'candlestick'])
    elif ctx.triggered_id == 'append-bar':
        # Times come back in the form they were given in, so a series built from
        # 'YYYY-MM-DD' strings reports strings.
        last = price['data'][-1]
        next_day = date.fromisoformat(last['time']) + timedelta(days=1)
        price['data'] = price['data'] + generate_random_ohlc(
            v0=last['close'], n=1, t0=next_day.isoformat()
        )

    return series


@callback(
    Output('chart-1', 'chartOptions'),
    Input('switch-background', 'n_clicks'),
    State('chart-1', 'chartOptions'),
    prevent_initial_call=True,
)
def switch_background(n_clicks, chart_options):
    chart_options = copy.deepcopy(chart_options)
    background = chart_options['layout']['background']
    background['color'] = switch_between(background['color'], BACKGROUNDS)
    return chart_options


@callback(
    Output('chart-2', 'series'),
    Input('move-price-line', 'n_clicks'),
    Input('move-markers', 'n_clicks'),
    Input('recolour-line', 'n_clicks'),
    State('chart-2', 'series'),
    prevent_initial_call=True,
)
def update_chart_2(price_line_clicks, marker_clicks, colour_clicks, series):
    series = copy.deepcopy(series)
    area, line = series[0], series[1]

    if ctx.triggered_id == 'move-price-line':
        area['priceLines'] = [{**area['priceLines'][0],
                               'price': 15 + random.uniform(-2, 2)}]
    elif ctx.triggered_id == 'move-markers':
        # A marker's time must match an existing data point, or it is dropped.
        area['markers'] = [
            {**marker, 'time': random.choice(AREA)['time']}
            for marker in area['markers']
        ]
    elif ctx.triggered_id == 'recolour-line':
        line['options'] = {**line['options'],
                           'color': switch_between(line['options'].get('color'),
                                                   ['#FFCC00', '#5555FF'])}

    return series


@callback(
    Output('readout', 'children'),
    Input('chart-1', 'crosshair'),
    Input('chart-1', 'click'),
    Input('chart-1', 'visibleLogicalRange'),
    Input('chart-1', 'visibleRange'),
    prevent_initial_call=True,
)
def show_events(crosshair, click, logical_range, time_range):
    def row(key, value):
        return html.Div(className='readout-row', children=[
            html.Span(key, className='readout-key'),
            html.Span(value, className='readout-value'),
        ])

    def describe(event):
        if not event:
            return '-'
        # `seriesData` is keyed by the id given in the `series` prop, and holds
        # the whole data point rather than a bare price.
        points = ' '.join(
            f'{series_id}={point.get("close", point.get("value")):.2f}'
            for series_id, point in sorted(event['seriesData'].items())
        )
        return f'{event["time"]} {points}'.strip() if event['time'] else '-'

    bars = '-' if not logical_range else (
        f'{logical_range["from"]:.1f} .. {logical_range["to"]:.1f}'
    )
    span = '-' if not time_range else f'{time_range["from"]} .. {time_range["to"]}'
    return [
        row('crosshair', describe(crosshair)),
        row('click', describe(click)),
        row('visible bars', bars),
        row('visible dates', span),
    ]


@callback(
    Output('extra-chart', 'children'),
    Input('add-chart', 'n_clicks'),
    prevent_initial_call=True,
)
def add_chart(n_clicks):
    return dash_tvlwc.Tvlwc(
        series=copy.deepcopy(CHART_2_SERIES),
        width='100%',
        height=180,
        chartOptions=CHARTS,
    )


if __name__ == '__main__':
    app.run(debug=True)
