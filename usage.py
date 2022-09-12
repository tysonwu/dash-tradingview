import dash_tvlwc
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc

from usage_dummy_data import candlestick_data as data

app = dash.Dash(__name__)

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
    'width': 1000,
    'height': 800
}

app.layout = html.Div([
    html.Div(children=[
        html.P(f'There are {len(data)} datapoints. Show only recent:'),
        dcc.Input(id='input', type='number', value=len(data)),
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
            chartOptions=chart_options
        ), style={'width': '900px', 'height': '900px', 'background': 'grey'}
    )
])


@app.callback(
    [Output('tv-chart', 'data')], 
    [Input('input-submit', 'n_clicks')],
    [State('input', 'value')]
)
def display_output(n, value):
    return [data[-value:]]


@app.callback(
    [Output('tv-chart', 'chartOptions')], 
    [Input('background-color-submit', 'n_clicks')],
    [
        State('background-color', 'value'),
        State('tv-chart', 'chartOptions'),
    ]
)
def display_output(n, value, option_state):
    chart_options = {
        'layout': {
            'background': {'type': Colors.backgroundType, 'color': value},
            'textColor': Colors.textColor,
        },
        'grid': {
            'vertLines': {'visible': False},
            'horzLines': {'visible': False},
        },
        'width': 1000,
        'height': 800
    }
    return [chart_options]



if __name__ == '__main__':
    app.run_server(debug=True)
