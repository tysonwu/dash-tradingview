# Reference

The Tradingview Lightweight Chart library is highly customizable in style. For the complete list of chart options and series options available, please refer to [the official API documentation](https://tradingview.github.io/lightweight-charts/docs/3.8).

```note
The supported version of Tradingview Lightweight Chart is v3.8.0. Make sure you consult the v3.8 document instead of latest version above 4.x.
```

## Dash Properties

**Configurable props**

|Property |Description  |
|---|---|
|`chartOptions`|a dict of options on chart canvas.|
|`seriesData`|a list series of list of timepoint dicts on series data.|
|`seriesTypes`|a list of series types, in the same order as `seriesData`.|
|`seriesOptions`|a list of series option dict for each series, in the same order as `seriesData`.|
|`seriesMarkers`|a list of list of markers dicts for each series, in the same order as `seriesData`.|
|`seriesPriceLines`|a list of list of price line dicts for each series, in the same order as `seriesData`.|
|`width`|width of outer container of the chart.|
|`height`|height of outer container of the chart.|

**Read-only props**

|Property |Description  |
|---|---|
|`id`|identifiable ID for the chart.|
|`crosshair`|position of last mouse hover on chart (crosshair coordinates).|
|`click`|position of last mouse click on chart (click coordinates).|
|`fullChartOptions`|full dict of applied chart options including default options.|
|`fullPriceScaleOptions`|full dict of applied series options including default options.|
|`timeRangeVisibleRange`|from-to dates of visible time range.|
|`timeRangeVisibleLogicalRange`|from-to numbers of visible time range.|
|`timeScaleWidth`|width of time scale.|
|`timeScaleHeight`|height of time scale.|
|`fullTimeScaleOptions`|full dict of applied time scale options including default options.|
