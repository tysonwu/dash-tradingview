import dash_tvlwc
import dash
from dash.dependencies import Input, Output
from dash import html, dcc

from usage_dummy_data import candlestick_data as data

app = dash.Dash(__name__)

colors = {
    'backgroundColor': '#1B2631',
    'lineColor': '#2962FF',
    'textColor': 'white',
    'areaTopColor': '#2962FF',
    'areaBottomColor': 'rgba(41, 98, 255, 0.28)',
}

app.layout = html.Div([
    html.P(f'There are {len(data)} datapoints. Show only recent:'),
    dcc.Input(id='input', type='number', value=len(data)),
    dash_tvlwc.Tvlwc(
        id='tv-chart',
        data=data,
        colors=colors,
    ),
])

@app.callback(
    [Output('tv-chart', 'data')], 
    [Input('input', 'value')]
)
def display_output(value):
    return [data[-value:]]


if __name__ == '__main__':
    app.run_server(debug=True)
