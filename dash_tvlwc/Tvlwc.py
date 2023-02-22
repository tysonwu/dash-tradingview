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

- click (dict; optional):
    Last-clicked on chart coordinates; read-only.

- crosshair (dict; optional):
    Crosshair coordinates; read-only.

- fullChartOptions (dict; optional):
    Full chart options including defaults; read-only.

- fullPriceScaleOptions (dict; optional):
    Full chart price scale options including defaults; read-only.

- fullSeriesOptions (dict; optional):
    Full series options including defaults; read-only.

- fullTimeScaleOptions (dict; optional):
    Full time scale options including defaults; read-only.

- height (string | number; default 400):
    Sets height of the parent div of the chart.

- priceScaleWidth (number; optional):
    Width of price scale; read-only.

- seriesData (list of list of dictss; optional):
    Data for the series.

- seriesMarkers (list of list of dictss; optional):
    Additional markers for the series.

- seriesOptions (list of dicts; optional):
    Options for the series.

- seriesPriceLines (list of list of dictss; optional):
    Additional price lines for the series.

- seriesTypes (list of a value equal to: 'bar', 'candlestick', 'area', 'baseline', 'line', 'histogram's; optional):
    Type of the series.

- timeRangeVisibleLogicalRange (dict; optional):
    Visible logical range (bar numbers); read-only.

- timeRangeVisibleRange (dict; optional):
    Visible time range (dates); read-only.

- timeScaleHeight (number; optional):
    Height of time scale; read-only.

- timeScaleWidth (number; optional):
    Width of time scale; read-only.

- width (string | number; default 600):
    Sets width of the parent div of the chart."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_tvlwc'
    _type = 'Tvlwc'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, chartOptions=Component.UNDEFINED, seriesData=Component.UNDEFINED, seriesTypes=Component.UNDEFINED, seriesOptions=Component.UNDEFINED, seriesMarkers=Component.UNDEFINED, seriesPriceLines=Component.UNDEFINED, crosshair=Component.UNDEFINED, click=Component.UNDEFINED, fullChartOptions=Component.UNDEFINED, fullPriceScaleOptions=Component.UNDEFINED, priceScaleWidth=Component.UNDEFINED, fullSeriesOptions=Component.UNDEFINED, timeRangeVisibleRange=Component.UNDEFINED, timeRangeVisibleLogicalRange=Component.UNDEFINED, timeScaleWidth=Component.UNDEFINED, timeScaleHeight=Component.UNDEFINED, fullTimeScaleOptions=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'chartOptions', 'click', 'crosshair', 'fullChartOptions', 'fullPriceScaleOptions', 'fullSeriesOptions', 'fullTimeScaleOptions', 'height', 'priceScaleWidth', 'seriesData', 'seriesMarkers', 'seriesOptions', 'seriesPriceLines', 'seriesTypes', 'timeRangeVisibleLogicalRange', 'timeRangeVisibleRange', 'timeScaleHeight', 'timeScaleWidth', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'chartOptions', 'click', 'crosshair', 'fullChartOptions', 'fullPriceScaleOptions', 'fullSeriesOptions', 'fullTimeScaleOptions', 'height', 'priceScaleWidth', 'seriesData', 'seriesMarkers', 'seriesOptions', 'seriesPriceLines', 'seriesTypes', 'timeRangeVisibleLogicalRange', 'timeRangeVisibleRange', 'timeScaleHeight', 'timeScaleWidth', 'width']
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
