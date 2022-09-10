import dash_tvlwc
import dash
from dash.dependencies import Input, Output
from dash import html

app = dash.Dash(__name__)

data = [
	{ 'time': '2018-12-22', 'value': 32.51 },
	{ 'time': '2018-12-23', 'value': 31.11 },
	{ 'time': '2018-12-24', 'value': 27.02 },
	{ 'time': '2018-12-25', 'value': 27.32 },
	{ 'time': '2018-12-26', 'value': 25.17 },
	{ 'time': '2018-12-27', 'value': 28.89 },
	{ 'time': '2018-12-28', 'value': 25.46 },
	{ 'time': '2018-12-29', 'value': 23.92 },
	{ 'time': '2018-12-30', 'value': 22.68 },
	{ 'time': '2018-12-31', 'value': 22.67 },
]

colors = {
    'backgroundColor': 'black',
    'lineColor': '#2962FF',
    'textColor': 'white',
    'areaTopColor': '#2962FF',
    'areaBottomColor': 'rgba(41, 98, 255, 0.28)',
}

app.layout = html.Div([
    dash_tvlwc.Tvlwc(
        id='tv-chart',
        data=data,
        colors=colors,
    ),
])

# @app.callback(Output('output', 'children'), [Input('input', 'value')])
# def display_output(value):
#     return 'You have entered {}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
