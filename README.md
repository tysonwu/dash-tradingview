<div style="text-align: center">
<h1>🎛 Dash Tradingview Lightweight Charts Component 📊</h1>
</div>

Dash Tradingview Lightweight Charts Components is a Dash component library. This component wraps the popular [TradingView Lightweight Charts by TradingView](https://github.com/tradingview/lightweight-charts) written in Typescript/Javascript, and renders it for use in Python [Dash](https://dash.plotly.com/) apps.

## Releases

| Date        | Tag|
| ----------- | ------ |
| 23 Feb 2023 | v0.1.1 |

## Installation

This package is available in PyPI:

```
pip install dash_tvlwc
```

## Demo

### Chart and series style options
- 1-to-1 chart and series option capability as in original lightweight chart
- See `./example/options.py`
![Options](./docs/options.png "Options")

### Interactivity with [Dash callbacks](https://dash.plotly.com/basic-callbacks)
- Modify data or styles on any triggers
- See `./example/interactivity.py`
![Interactivity](./docs/interactivity.gif "Interactivity")

### Minimal example
```python
series_data = [{'time': '2020-01-01', 'value': 10.0}, ...]

series_options = [{
    'lineColor': '#FFAA30',
    'topColor': '#2962FF',
    'priceLineWidth': 3,
    'priceLineColor': 'red'
}]

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

dash_tvlwc.Tvlwc(
    id='bar-chart',
    seriesData=[series_data],
    seriesTypes=['bar'],
    seriesOptions=[series_options]
    width='100%',
    chartOptions=chart_options
)
```

## References: Chart properties

The Tradingview Lightweight Chart library is highly customizable in style. For the complete list of chart options and series options available, please refer to [the official API document](https://tradingview.github.io/lightweight-charts/docs/api).

**Configurable props**

- `id`: identifiable ID for the chart.
- `chartOptions`: a dict of options on chart canvas.
- `seriesData`: a list series of list of timepoint dicts on series data.
- `seriesTypes`: a list of series types, in the same order as `seriesData`.
- `seriesOptions`: a list of series option dict for each series, in the same order as `seriesData`.
- `seriesMarkers`: a list of list of markers dicts for each series, in the same order as `seriesData`.
- `seriesPriceLines`: a list of list of price line dicts for each series, in the same order as `seriesData`.
- `width`: width of outer container of the chart.
- `height`: height of outer container of the chart.

**Read-only props**
- `crosshair`: position of last mouse hover on chart (crosshair coordinates).
- `click`: position of last mouse click on chart (click coordinates).
- `fullChartOptions`: full dict of applied chart options including default options.
- `fullPriceScaleOptions`: full dict of applied series options including default options.
- `timeRangeVisibleRange`: from-to dates of visible time range.
- `timeRangeVisibleLogicalRange` from-to numbers of visible time range.
- `timeScaleWidth`: width of time scale.
- `timeScaleHeight`: height of time scale.
- `fullTimeScaleOptions`: full dict of applied time scale options including default options.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## Development

1. Install Dash and its dependencies: https://dash.plotly.com/installation
2. Run demonstration script with `python example/usage.py`
3. Visit the demo Dash app at http://localhost:8050 in your web browser

### Install dependencies

If you have selected install_dependencies during the prompt, you can skip this part.

1. Install npm packages
    ```
    $ npm install
    ```
2. Create a virtual env and activate.
    ```
    $ virtualenv venv
    $ . venv/bin/activate
    ```
    _Note: venv\Scripts\activate for windows_

3. Install python packages required to build components.
    ```
    $ pip install -r requirements.txt
    ```
4. Install the python packages for testing (optional)
    ```
    $ pip install -r tests/requirements.txt
    ```