"""Hosted showcase for dash-tvlwc.

Run from the repository root:

    PYTHONPATH=. python demo/app.py
"""
import copy
import random
from datetime import date, timedelta

import dash
from dash import Input, Output, State, callback, ctx, dcc, html

import dash_tvlwc
import theme
from data_generator import generate_random_ohlc, generate_random_series
from theme import CHART_OPTIONS, merge

# The hero chart names a formatter registered in assets/tvlwc_functions.js.
# Options that must be JavaScript functions cannot cross the Python boundary.
HERO_OPTIONS = merge(CHART_OPTIONS, {'localization': {'priceFormatter': 'usd'}})

# Two console layers rather than a decorative colour, so the theme toggle stays
# inside the palette.
LAYERS = [theme.CARD, theme.ACCENT]


def chart(component_id, series, options=None, height=240, **kwargs):
    return dash_tvlwc.Tvlwc(
        id=component_id,
        series=series,
        width='100%',
        height=height,
        chartOptions=merge(CHART_OPTIONS, options or {}),
        **kwargs,
    )


hero = theme.panel(
    'Live chart', 'series rewritten every 500 ms',
    html.Div(className='hero', children=[
        html.Div(className='hero-readout', children=[
            html.Span(id='chart-price', className='hero-price'),
            html.Span(id='chart-date', className='hero-date'),
        ]),
        dash_tvlwc.Tvlwc(
            id='tv-chart-1',
            series=[{
                'id': 'main',
                'type': 'candlestick',
                'data': generate_random_ohlc(100, n=200),
                'options': {'upColor': theme.GREEN, 'downColor': theme.RED,
                            'borderVisible': False,
                            'wickUpColor': theme.GREEN, 'wickDownColor': theme.RED},
            }],
            width='100%',
            height=320,
            chartOptions=HERO_OPTIONS,
            # Crosshair reporting is a server round trip per report, so it is off
            # unless asked for. `reportThrottle` coalesces; zero batches to one
            # report per animation frame.
            subscribeCrosshair=True,
            reportThrottle=50,
        ),
    ]),
    theme.toolbar(
        theme.button('Candlestick / Line', 'change-chart-type'),
        theme.button('Switch layer', 'change-theme'),
    ),
)


bar = theme.panel(
    'Bar', 'series[].type = bar',
    chart('bar-chart', [{
        'id': 'price',
        'type': 'bar',
        'data': generate_random_ohlc(v0=100, n=50),
        'options': {'upColor': theme.GREEN, 'downColor': theme.RED,
                    'thinBars': False},
    }]),
)


# Data points carrying only `time` are whitespace: they reserve the slot and
# render as a gap. Do not use None values for this.
candles = generate_random_ohlc(v0=1, n=50, ret=0.1)
candles = [{'time': p['time']} if 12 < i < 20 or i > 45 else p
           for i, p in enumerate(candles)]

candlestick = theme.panel(
    'Candlestick', 'whitespace points -> gaps',
    chart('candlestick-chart', [{
        'id': 'price',
        'type': 'candlestick',
        'data': candles,
        'options': {
            'upColor': theme.ORANGE,
            'downColor': theme.PURPLE,
            'borderVisible': False,
            'wickUpColor': theme.ORANGE,
            'wickDownColor': theme.PURPLE,
        },
    }]),
)


area = theme.panel(
    'Area', "localization.priceFormatter = 'usd'",
    chart('area-chart', [{
        'id': 'price',
        'type': 'area',
        'data': generate_random_series(v0=15, n=50),
        'options': {
            'lineColor': theme.BLUE,
            'lineWidth': 2,
            'topColor': 'rgba(10, 132, 255, 0.35)',
            'bottomColor': 'rgba(10, 132, 255, 0.02)',
            'priceLineColor': theme.BORDER,
        },
    }], {'localization': {'priceFormatter': 'usd'}}),
)


baseline_data = generate_random_series(v0=5000, n=50)
baseline_mean = sum(p['value'] for p in baseline_data) / len(baseline_data)
baseline_max = max(p['value'] for p in baseline_data)

# Colour here is semantic: above and below the baseline are different states.
baseline = theme.panel(
    'Baseline', "priceScaleId = 'left'",
    chart('baseline-chart', [{
        'id': 'price',
        'type': 'baseline',
        'data': baseline_data,
        'options': {
            'baseValue': {'type': 'price', 'price': baseline_mean},
            'topLineColor': theme.GREEN,
            'topFillColor1': 'rgba(48, 209, 88, 0.28)',
            'topFillColor2': 'rgba(48, 209, 88, 0.02)',
            'bottomLineColor': theme.RED,
            'bottomFillColor1': 'rgba(255, 69, 58, 0.02)',
            'bottomFillColor2': 'rgba(255, 69, 58, 0.28)',
            'lineWidth': 2,
            'priceScaleId': 'left',
        },
        'priceLines': [{
            'price': baseline_max, 'color': theme.BORDER, 'lineStyle': 2,
            'title': 'MAX', 'axisLabelVisible': True,
        }],
    }], {
        'rightPriceScale': {'visible': False},
        'leftPriceScale': {'visible': True, 'borderColor': theme.BORDER},
        'timeScale': {'visible': False},
    }),
)


line_data = generate_random_series(v0=1, n=50, ret=0.1)
volume_data = generate_random_series(v0=100, n=50, ret=0.05)
for point in volume_data:
    # Per-point `color` overrides the series colour. Do not add a second series
    # or use markers to recolour bars.
    point['color'] = random.choice(['rgba(48, 209, 88, 0.55)',
                                    'rgba(255, 69, 58, 0.55)'])

line_and_volume = theme.panel(
    'Line and volume', 'priceScaleOptions.scaleMargins',
    chart('line-chart', [
        {
            'id': 'price',
            'type': 'line',
            'data': line_data,
            'options': {'lineWidth': 2, 'color': theme.CYAN},
            'markers': [
                {'time': line_data[15]['time'], 'position': 'aboveBar',
                 'color': theme.ORANGE, 'shape': 'circle', 'text': 'Signal'},
                {'time': line_data[20]['time'], 'position': 'belowBar',
                 'color': theme.GREEN, 'shape': 'arrowUp', 'text': 'Buy'},
            ],
        },
        {
            'id': 'volume',
            'type': 'histogram',
            'data': volume_data,
            'options': {
                'priceFormat': {'type': 'volume'},
                'priceScaleId': '',
                'priceLineVisible': False,
                'lastValueVisible': False,
            },
            # `scaleMargins` belongs to the price scale, not to the series.
            'priceScaleOptions': {'scaleMargins': {'top': 0.9, 'bottom': 0}},
        },
    ]),
)


histogram_data = generate_random_series(v0=100, n=50, ret=0.3)
for i in (5, 12, 13, 14, 20, 33, 34, 46):
    histogram_data[i]['color'] = theme.MINT

histogram = theme.panel(
    'Histogram', 'per-point color, base = 100',
    chart('histogram-chart', [{
        'id': 'value',
        'type': 'histogram',
        'data': histogram_data,
        'options': {
            'color': theme.PURPLE,
            'base': 100,
            'priceLineVisible': False,
            'lastValueVisible': False,
        },
    }]),
)


app = dash.Dash(__name__, external_stylesheets=[theme.FONTS])
app.layout = html.Div([
    dcc.Interval(id='timer', interval=500),
    theme.topbar('dash-tvlwc', 'lightweight-charts 5.2.1 · dash-tvlwc 0.2.0-dev'),
    html.Main(className='shell', children=[
        html.H1('Tradingview Lightweight Charts for Dash', className='page-title'),
        theme.prose(dcc.Markdown('''
        A custom [Dash](https://dash.plotly.com/) component wrapping
        [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts)
        for use from Python. Source on
        [Github](https://github.com/tysonwu/dash-tradingview), released on
        [PyPI](https://pypi.org/project/dash-tvlwc/).
        ''', link_target='_blank')),
        html.Div(hero, style={'marginTop': '16px'}),
        html.H2('Styling options', className='section-title'),
        html.Div(className='panel-grid options-grid', children=[
            bar, candlestick, area, baseline, line_and_volume, histogram,
        ]),
        html.Div(className='footer', children=[
            html.Span('By Tyson Wu'),
            html.Span('MIT licensed · charts by TradingView'),
        ]),
    ]),
])


@callback(
    Output('tv-chart-1', 'chartOptions'),
    Input('change-theme', 'n_clicks'),
    State('tv-chart-1', 'chartOptions'),
    prevent_initial_call=True,
)
def change_layer(n_clicks, chart_options):
    current = chart_options['layout']['background']['color']
    nxt = LAYERS[1] if current == LAYERS[0] else LAYERS[0]
    return merge(chart_options, {'layout': {'background': {'type': 'solid',
                                                           'color': nxt}}})


@callback(
    Output('tv-chart-1', 'series'),
    Input('change-chart-type', 'n_clicks'),
    Input('timer', 'n_intervals'),
    State('tv-chart-1', 'series'),
    prevent_initial_call=True,
)
def update_main_chart(n_clicks, n_intervals, series):
    """Everything about a series lives in one `series` prop, so the type switch
    and the ticker share a callback and dispatch on `ctx.triggered_id`. Two
    callbacks cannot write the same prop without `allow_duplicate=True`.
    """
    series = copy.deepcopy(series)
    main = series[0]

    if ctx.triggered_id == 'change-chart-type':
        if main['type'] == 'candlestick':
            main['type'] = 'line'
            main['data'] = generate_random_series(100, n=200)
            main['options'] = {'lineWidth': 2, 'color': theme.CYAN}
        else:
            main['type'] = 'candlestick'
            main['data'] = generate_random_ohlc(100, n=200)
            main['options'] = {'upColor': theme.GREEN, 'downColor': theme.RED,
                               'borderVisible': False,
                               'wickUpColor': theme.GREEN,
                               'wickDownColor': theme.RED}
        return series

    # Sliding window: append a bar, drop the oldest. Times come back in the form
    # they were given in, so a series built from 'YYYY-MM-DD' strings reports
    # strings. Rewriting the whole series on a timer is the only route today;
    # the `tick` prop will replace it with an incremental append.
    last = main['data'][-1]
    next_day = (date.fromisoformat(last['time']) + timedelta(days=1)).isoformat()
    if main['type'] == 'candlestick':
        new_point = generate_random_ohlc(v0=last['close'], n=1, t0=next_day)
    else:
        new_point = generate_random_series(v0=last['value'], n=1, t0=next_day)
    main['data'] = main['data'][1:] + new_point
    return series


@callback(
    Output('chart-date', 'children'),
    Output('chart-price', 'children'),
    Input('tv-chart-1', 'crosshair'),
    prevent_initial_call=True,
)
def crosshair_move(crosshair):
    # `seriesData` is keyed by the id given in the `series` prop, and holds the
    # whole data point rather than a bare price.
    crosshair = crosshair or {}
    point = crosshair.get('seriesData', {}).get('main')
    time = crosshair.get('time')

    if not point or not time:
        return 'Hover the chart for date and price', ''

    value = point.get('close', point.get('value'))
    return time, f'${value:,.2f}'


if __name__ == '__main__':
    app.run(debug=True)
