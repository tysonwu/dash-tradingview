import random
from datetime import datetime, timedelta

import dash_tvlwc
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc, ctx

from dash_tvlwc.types import ColorType, SeriesType
from data_generator import generate_random_ohlc, generate_random_series


main_panel = [
    html.Div(style={'position': 'relative', 'width': '100%', 'height': '100%', 'marginBottom': '30px'}, children=[
        html.Div(children=[
            dash_tvlwc.Tvlwc(
                id='tv-chart-1',
                seriesData=[generate_random_ohlc(100, n=100)],
                seriesTypes=[SeriesType.Candlestick],
                width='99%',
                chartOptions={
                    'layout': {
                        'background': {'type': ColorType.Solid, 'color': '#1B2631'},
                        'textColor': 'white',
                    },
                    'grid': {
                        'vertLines': {'visible': True, 'color': 'rgba(255,255,255,0.1)'},
                        'horzLines': {'visible': True, 'color': 'rgba(255,255,255,0.1)'},
                    },
                    'localization': {
                        'locale': 'en-US',
                        'priceFormatter': "(function(price) { return '$' + price.toFixed(2); })"
                    }
                },
            ),
        ], style={'width': '100%', 'height': '100%', 'left': 0, 'top': 0}),
        html.Div(id='chart-info', children=[
            html.Span(id='chart-price', style={'fontSize': '60px', 'fontWeight': 'bold'}),
            html.Span(id='chart-date', style={'fontSize': 'small'}),
        ], style={'position': 'absolute', 'left': 0, 'top': 0, 'zIndex': 10, 'color': 'white', 'padding': '10px'})
    ]),
    html.Div(children=[
        html.Button('Candlestick / Line chart', id='change-chart-type'),
        html.Button('Change theme', id='change-theme'),
    ], style={'display': 'block'})
]


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


app = dash.Dash(__name__, external_stylesheets=['./assets/stylesheet.css'])
app.layout = html.Div([
    dcc.Interval(id='timer', interval=500),
    html.Div(className='container', children=[
        html.Div(className='main-container', children=[
            html.H1('🎛 Dash Tradingview Lightweight Charts Component 📊'),
            dcc.Markdown('''
            You are looking at a [Dash](https://dash.plotly.com/) app.
            Dash Tradingview Lightweight Charts Components is a custom Dash component
            that wraps the popular [TradingView Lightweight Charts by TradingView](https://github.com/tradingview/lightweight-charts),
            and renders it for use in Python Dash.

            Source code is available on [Github](https://github.com/tysonwu/dash-tradingview).
            Availble on [PyPI](https://pypi.org/project/dash-tvlwc/).
            ''', link_target='_blank'),
            html.Div(children=main_panel),
            html.H2('Highly customizable styling options'),
            html.Div(className='options-container', children=[
                html.Div(className='one', children=panel1),
                html.Div(className='two', children=panel2),
                html.Div(className='three', children=panel3),
                html.Div(className='four', children=panel4),
                html.Div(className='five', children=panel5),
                html.Div(className='six', children=panel6),
            ])
        ]),
        html.Span('By Tyson Wu, 2023')
    ])
])


# callbacks to demo
@app.callback(
    [
        Output('tv-chart-1', 'chartOptions'),
        Output('chart-info', 'style'),
    ],
    [Input('change-theme', 'n_clicks')],
    [
        State('tv-chart-1', 'chartOptions'),
        State('chart-info', 'style'),
    ],
    prevent_initial_call=True
)
def change_props(n, current_chart_options, chart_info_style):
    if current_chart_options['layout']['background']['color'] == '#1B2631':
        current_chart_options = {
            'layout': {
                'background': {'type': ColorType.Solid, 'color': '#dddddd'},
                'textColor': '#111111',
            },
            'grid': {
                'vertLines': {'visible': True, 'color': 'rgba(0,0,0,0.1)'},
                'horzLines': {'visible': True, 'color': 'rgba(0,0,0,0.1)'},
            }
        }
        chart_info_style['color'] = '#111111'
    else:
        current_chart_options = {
            'layout': {
                'background': {'type': ColorType.Solid, 'color': '#1B2631'},
                'textColor': 'white',
            },
            'grid': {
                'vertLines': {'visible': True, 'color': 'rgba(255,255,255,0.1)'},
                'horzLines': {'visible': True, 'color': 'rgba(255,255,255,0.1)'},
            },
        }
        chart_info_style['color'] = '#bbbbbb'

    return [current_chart_options, chart_info_style]


@app.callback(
    [
        Output('tv-chart-1', 'seriesData'),
        Output('tv-chart-1', 'seriesTypes'),
    ],
    [
        Input('change-chart-type', 'n_clicks'),
        Input('timer', 'n_intervals')
    ],
    [
        State('tv-chart-1', 'seriesData'),
        State('tv-chart-1', 'seriesTypes'),
    ],
    prevent_initial_call=True
)
def change_props(n, interval, series_data, series_type):
    if ctx.triggered_id == 'timer':
        last_close_date = series_data[0][-1]['time']
        last_close_dt = datetime(last_close_date['year'], last_close_date['month'], last_close_date['day'])
        if series_type == [SeriesType.Candlestick]:
            new_datapoint = generate_random_ohlc(
                t0=(last_close_dt + timedelta(days=1)).strftime('%Y-%m-%d'),
                v0=series_data[0][-1]['close'], n=1
            )
            series_data[0].extend(new_datapoint)
        else:
            new_datapoint = generate_random_series(
                t0=(last_close_dt + timedelta(days=1)).strftime('%Y-%m-%d'),
                v0=series_data[0][-1]['value'], n=1
            )
            series_data[0].extend(new_datapoint)
        series_data[0] = series_data[0][1:]
        return [series_data, series_type]

    elif ctx.triggered_id == 'change-chart-type':
        if series_type == [SeriesType.Candlestick]:
            series_type = [SeriesType.Line]
            series_data = [generate_random_series(100, n=100)]
        else:
            series_type = [SeriesType.Candlestick]
            series_data = [generate_random_ohlc(100, n=100)]
        return [series_data, series_type]



@app.callback(
    [
        Output('chart-date', 'children'),
        Output('chart-price', 'children'),
    ],
    [Input('tv-chart-1', 'crosshair')],
    [State('tv-chart-1', 'seriesTypes')],
    prevent_initial_call=True
)
def crosshair_move(crosshair, series_types):
    time = crosshair.get('time')
    prices = crosshair['seriesPrices']

    if time is not None:
        time = datetime(time['year'], time['month'], time['day']).strftime('%Y-%m-%d') if time is not None else time
        time = f'{time}' if time is not None else None

    if prices:
        if series_types == [SeriesType.Candlestick]:
            prices = f"{prices['0']['close']:.2f}"
        else:
            prices = f"{prices['0']:.2f}"

    if not time and not prices:
        time = 'Hover on the plot to see date and price details.'

    return [time, prices]


if __name__ == '__main__':
    app.run_server(debug=True)
