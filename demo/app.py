import random
from datetime import datetime, timedelta

import dash_tvlwc
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc

from dash_tvlwc.types import ColorType, SeriesType
from data_generator import generate_random_ohlc, generate_random_series


panel1 = [
    html.Div(style={'position': 'relative', 'width': '100%', 'height': '100%', 'marginBottom': '30px'}, children=[
        html.Div(children=[
            dash_tvlwc.Tvlwc(
                id='tv-chart-1',
                seriesData=[generate_random_ohlc(100, n=50)],
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
        html.Button('Change theme', id='change-theme')
    ], style={'display': 'block'})
]

app = dash.Dash(__name__, external_stylesheets=['./assets/stylesheet.css'])
app.layout = html.Div([
    dcc.Interval(id='timer', interval=1000),
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
            html.Div(children=panel1),
        ]),
        html.P('By Tyson Wu, 2023')
    ])
])


# callbacks to demo
@app.callback(
    [
        Output('tv-chart-1', 'seriesData'),
        Output('tv-chart-1', 'chartOptions'),
        Output('chart-info', 'style'),
    ],
    [Input('change-theme', 'n_clicks')],
    [
        State('tv-chart-1', 'seriesData'),
        State('tv-chart-1', 'chartOptions'),
        State('chart-info', 'style'),
    ],
    prevent_initial_call=True
)
def change_props(n, series_data, current_chart_options, chart_info_style):
    # parse date time in tradingview
    last_close_date = series_data[0][-1]['time']
    last_close_dt = datetime(last_close_date['year'], last_close_date['month'], last_close_date['day'])
    new_datapoint = generate_random_ohlc(
        t0=(last_close_dt + timedelta(days=1)).strftime('%Y-%m-%d'),
        v0=series_data[0][-1]['close'], n=1
    )
    series_data[0].extend(new_datapoint)

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

    return [series_data, current_chart_options, chart_info_style]


@app.callback(
    [
        Output('chart-date', 'children'),
        Output('chart-price', 'children'),
    ],
    [Input('tv-chart-1', 'crosshair')],
    prevent_initial_call=True
)
def crosshair_move(crosshair):
    time = crosshair.get('time')
    prices = crosshair['seriesPrices']

    if time is not None:
        time = datetime(time['year'], time['month'], time['day']).strftime('%Y-%m-%d') if time is not None else time
        time = f'{time}' if time is not None else None

    if prices:
        prices = f"{prices['0']['close']:.2f}"

    if not time and not prices:
        time = 'Hover on the plot to see date and price details.'

    return [time, prices]


if __name__ == '__main__':
    app.run_server(debug=True)
