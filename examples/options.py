"""Chart options and series options, one panel per series type.

Run from the repository root:

    python example/options.py
"""
import random

from dash import Dash, html

import dash_tvlwc
import theme
from data_generator import generate_random_ohlc, generate_random_series
from theme import CHART_OPTIONS, merge


def chart(component_id, series, options=None, height=240):
    return dash_tvlwc.Tvlwc(
        id=component_id,
        series=series,
        width='100%',
        height=height,
        chartOptions=merge(CHART_OPTIONS, options or {}),
    )


# Every series carries its own id, type, data and options. The id is what keys
# the `crosshair`, `click` and `fullSeriesOptions` payloads.
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


# `priceFormatter` must be a JavaScript function, which cannot cross the Python
# boundary. Name a function registered in assets/tvlwc_functions.js instead.
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
            # Squeeze the volume into the bottom tenth of the pane.
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

app = Dash(__name__, external_stylesheets=[theme.FONTS])
app.layout = html.Div([
    theme.topbar('Chart and series options',
                 'lightweight-charts 5.2.1 · dash-tvlwc 0.2.0-dev'),
    html.Main(className='shell', children=[
        html.Div(className='panel-grid options-grid', children=[
            bar, candlestick, area, baseline, line_and_volume, histogram,
        ]),
    ]),
])

if __name__ == '__main__':
    app.run(debug=True)
