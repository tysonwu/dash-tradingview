import random

import dash_tvlwc
import dash
from dash.dependencies import Input, Output, State
from dash import html

from example.data_generator import generate_random_ohlc, generate_random_series

app = dash.Dash(__name__, external_stylesheets=['./assets/stylesheet.css'])

chart_options = {
    'layout': {
        'background': {'type': 'solid', 'color': '#1B2631'},
        'textColor': 'white',
    },
    'grid': {
        'vertLines': {'visible': False},
        'horzLines': {'visible': False},
    },
    'localization': {'locale': 'en-US'}
}

panel1 = [
    html.H2('Bar'),
    dash_tvlwc.Tvlwc(
        id='bar-chart',
        seriesData=[generate_random_ohlc(v0=100, n=50)],
        seriesTypes=['bar'],
        width='100%',
        chartOptions=chart_options
    )
]


p2_series = generate_random_ohlc(v0=1, n=50, ret=0.1)
p2_series = [{'time': v['time']} if 12 < idx < 20 or idx > 45 else v for idx, v in enumerate(p2_series)]
panel2 = [
    html.H2('Candlestick'),
    dash_tvlwc.Tvlwc(
        id='candlestick-chart',
        seriesData=[p2_series],
        seriesTypes=['candlestick'],
        seriesOptions=[{
            'downColor': '#a6269a',
            'upColor': '#ffaa30',
            'borderColor': 'black',
            'wickColor': 'black'
        }],
        width='100%',
        chartOptions={'layout': {'background': {'type': 'solid', 'color': 'white'}}}
    )
]


panel3 = [
    html.H2('Area'),
    dash_tvlwc.Tvlwc(
        id='area-chart',
        seriesData=[generate_random_series(v0=15, n=50)],
        seriesTypes=['area'],
        seriesOptions=[{
            'lineColor': '#FFAA30',
            'topColor': '#2962FF',
            'bottomColor': 'rgba(180, 98, 200, 0.1)',
            'priceLineWidth': 3,
            'priceLineColor': 'red'
        }],
        width='100%',
        chartOptions=chart_options
    )
]


p4_series = generate_random_series(v0=5000, n=50)
p4_mean = sum([p['value'] for p in p4_series]) / 50
p4_max = max([p['value'] for p in p4_series])
price_lines = [{'price': p4_max, 'color': '#2962FF', 'lineStyle': 0, 'title': 'MAX PRICE', 'axisLabelVisible': True}]
panel4 = [
    html.H2('Baseline'),
    dash_tvlwc.Tvlwc(
        id='baseline-chart',
        seriesData=[p4_series],
        seriesTypes=['baseline'],
        seriesOptions=[{
            'baseValue': {'type': 'price', 'price': p4_mean},
            'topFillColor1': 'black',
            'topFillColor2': 'rgba(255,255,255,0)',
            'topLineColor': 'black',
            'crosshairMarkerRadius': 8,
            'lineWidth': 5,
            'priceScaleId': 'left'
        }],
        seriesPriceLines=[price_lines],
        width='100%',
        chartOptions={
            'rightPriceScale': {'visible': False},
            'leftPriceScale': {'visible': True, 'borderColor': 'rgba(197, 203, 206, 1)',},
            'timeScale': {'visible': False},
            'grid': {'vertLines': {'visible': False}, 'horzLines': {'style': 0, 'color': 'black'}},
        }
    )
]


# add markers and add color to volume bar
p5_series = generate_random_series(v0=1, n=50, ret=0.1)
markers = [
    {'time': p5_series[15]['time'], 'position': 'aboveBar', 'color': '#f68410', 'shape': 'circle', 'text': 'Signal'},
    {'time': p5_series[20]['time'], 'position': 'belowBar', 'color': 'white', 'shape': 'arrowUp', 'text': 'Buy'}
]
p5_series_volume = generate_random_series(v0=100, n=50, ret=0.05)
for i in p5_series_volume:
    i['color'] = random.choice(['rgba(0, 150, 136, 0.8)', 'rgba(255,82,82, 0.8)'])

panel5 = [
    html.H2('Line and volume'),
    dash_tvlwc.Tvlwc(
        id='line-chart',
        seriesData=[p5_series, p5_series_volume],
        seriesTypes=['line', 'histogram'],
        seriesOptions=[
            {
                'lineWidth': 1
            },
            {
                'color': '#26a69a',
                'priceFormat': {'type': 'volume'},
                'priceScaleId': '',
                'scaleMargins': {'top': 0.9, 'bottom': 0},
                'priceLineVisible': False
            },
        ],
        seriesMarkers=[markers],
        width='100%',
        chartOptions=chart_options
    )
]


p6_series = generate_random_series(v0=100, n=50, ret=0.3)
for idx, _ in enumerate(p6_series):
    if idx in [5,12,13,14,20,33,34,46]:
        p6_series[idx]['color'] = 'white'

panel6 = [
    html.H2('Histogram'),
    dash_tvlwc.Tvlwc(
        id='histogram-chart',
        seriesData=[p6_series],
        seriesTypes=['histogram'],
        seriesOptions=[{
            'color': '#ff80cc',
            'base': 100,
            'priceLineVisible': False,
            'lastValueVisible': False
        }],
        width='100%',
        chartOptions={'layout': {'textColor': '#ff80cc', 'background': {'type': 'solid', 'color': 'black'}}}
    )
]

app.layout = html.Div([
    html.H1('Chart options and series options'),
    html.Div(className='container', children=[
        html.Div(className='one', children=panel1),
        html.Div(className='two', children=panel2),
        html.Div(className='three', children=panel3),
        html.Div(className='four', children=panel4),
        html.Div(className='five', children=panel5),
        html.Div(className='six', children=panel6),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
