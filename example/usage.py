import dash_tvlwc
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc

from example.data_generator import generate_random_ohlc, generate_random_series

app = dash.Dash(__name__, external_stylesheets=['./assets/stylesheet.css'])

class Colors:
    backgroundType = 'solid'
    backgroundColor = '#1B2631'
    lineColor = '#2962FF'
    textColor = 'white'
    areaTopColor = '#2962FF'
    areaBottomColor = 'rgba(41, 98, 255, 0.28)'


chart_options = {
    'layout': {
        'background': {'type': Colors.backgroundType, 'color': Colors.backgroundColor},
        'textColor': Colors.textColor,
    },
    'grid': {
        'vertLines': {'visible': False},
        'horzLines': {'visible': False},
    },
}

# seriesType options: https://tradingview.github.io/lightweight-charts/docs/api/interfaces/SeriesOptionsMap
random_candlestick_data = generate_random_ohlc(100, n=100)
random_series_data = generate_random_series(100, n=100)

data = [
    {
        'seriesData': random_candlestick_data,
        'seriesType': 'candlestick',
    },
    {
        'seriesData': random_series_data,
        'seriesType': 'area',
    }
]

panel0 = [
    html.Div(children=[
        html.P(f'There are {len(random_candlestick_data)} datapoints. Show only recent:'),
        dcc.Input(id='input', type='number', value=len(random_candlestick_data)),
        html.Button('Submit', id='input-submit'),
    ]),
    html.Div(children=[
        html.P(f'Change background color'),
        dcc.Input(id='background-color', type='text', value='#1B2631'),
        html.Button('Submit', id='background-color-submit'),
    ]),
    html.Div(
        dash_tvlwc.Tvlwc(
            id='tv-chart',
            data=data,
            width='100%',
            chartOptions=chart_options
        ), style={'background': 'grey'}
    )
]

panel1 = [
    html.H2('Bar'),
    dash_tvlwc.Tvlwc(
        id='bar-chart',
        data=[{
            'seriesData': generate_random_ohlc(v0=100, n=50),
            'seriesType': 'bar',
            'seriesOptions': {}
        }],
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
        data=[{
            'seriesData': p2_series,
            'seriesType': 'candlestick',
            'seriesOptions': {'downColor': '#a6269a', 'upColor': '#ffaa30',
                              'borderColor': 'black', 'wickColor': 'black' }
        }],
        width='100%',
        chartOptions={'layout': {'background': {'type': 'solid', 'color': 'white'}}}
    )
]


panel3 = [
    html.H2('Area'),
    dash_tvlwc.Tvlwc(
        id='area-chart',
        data=[{
            'seriesData': generate_random_series(v0=15, n=50),
            'seriesType': 'area',
            'seriesOptions': { 'lineColor': '#FFAA30', 'topColor': '#2962FF',
                              'bottomColor': 'rgba(180, 98, 200, 0.1)', 'priceLineWidth': 3,
                              'priceLineColor': 'red', }
        }],
        width='100%',
        chartOptions=chart_options
    )
]


p4_series = generate_random_series(v0=5000, n=50)
p4_mean = sum([p['value'] for p in p4_series]) / 50
panel4 = [
    html.H2('Baseline'),
    dash_tvlwc.Tvlwc(
        id='baseline-chart',
        data=[{
            'seriesData': p4_series,
            'seriesType': 'baseline',
            'seriesOptions': {'baseValue': {'type': 'price', 'price': p4_mean},
                              'topFillColor1': 'rgba(255,255,255,0.9)', 'topFillColor2': 'rgba(255,255,255,0)',
                              'topLineColor': 'white', 'crosshairMarkerRadius': 8, 'lineWidth': 5}
        }],
        width='100%',
        chartOptions=chart_options
    )
]


# some random whitespace data
panel5 = [
    html.H2('Line'),
    dash_tvlwc.Tvlwc(
        id='line-chart',
        data=[{
            'seriesData': generate_random_series(v0=1, n=50, ret=0.1),
            'seriesType': 'line',
            'seriesOptions': {}
        }],
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
        data=[{
            'seriesData': p6_series,
            'seriesType': 'histogram',
            'seriesOptions': {'color': '#ff80cc', 'base': 100, 'priceLineVisible': False,
                              'lastValueVisible': False}
        }],
        width='100%',
        chartOptions={'layout': {'textColor': '#ff80cc', 'background': {'type': 'solid', 'color': 'black'}}}
    )
]

app.layout = html.Div([
    html.H1('Demo'),
    html.Div(className='one', children=panel0),
    html.Div(className='container', children=[
        html.Div(className='one', children=panel1),
        html.Div(className='two', children=panel2),
        html.Div(className='three', children=panel3),
        html.Div(className='four', children=panel4),
        html.Div(className='five', children=panel5),
        html.Div(className='six', children=panel6),
    ])
])


# callback to change candlestick data
@app.callback(
    [Output('tv-chart', 'data')],
    [Input('input-submit', 'n_clicks')],
    [State('input', 'value'), State('tv-chart', 'data')]
)
def display_output(n, value, series_data):
    series_data[0]['seriesData'] = data[0]['seriesData'][-value:]
    return [series_data]


# callback to change background color
@app.callback(
    [Output('tv-chart', 'chartOptions')],
    [Input('background-color-submit', 'n_clicks')],
    [State('background-color', 'value'), State('tv-chart', 'chartOptions')]
)
def change_props(n, value, current_chart_options):
    current_chart_options['layout']['background']['color'] = value
    return [current_chart_options]



if __name__ == '__main__':
    app.run_server(debug=True)
