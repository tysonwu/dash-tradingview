# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tvlwc(Component):
    """A Tvlwc component.
Tradingview Lightweight Chart object

Keyword arguments:

- id (string; optional):
    The ID of this component.

- chartOptions (dict; optional):
    Object containing all chart options See
    https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions
    for possible options.

- data (list of dicts; optional):
    The data for the series.

    `data` is a list of dicts with keys:

    - seriesData (list of dicts; optional)

    - seriesOptions (dict; optional)

    - seriesType (a value equal to: 'Candlestick', 'Area'; optional)

- height (string | number; default 400):
    Sets height of the parent div of the chart.

- width (string | number; default 600):
    Sets width of the parent div of the chart."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_tvlwc'
    _type = 'Tvlwc'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, chartOptions=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'chartOptions', 'data', 'height', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'chartOptions', 'data', 'height', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tvlwc, self).__init__(**args)
