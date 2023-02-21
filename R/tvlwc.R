# AUTO GENERATED FILE - DO NOT EDIT

#' @export
tvlwc <- function(id=NULL, chartOptions=NULL, click=NULL, crosshair=NULL, fullChartOptions=NULL, fullPriceScaleOptions=NULL, fullSeriesOptions=NULL, fullTimeScaleOptions=NULL, height=NULL, priceScaleWidth=NULL, seriesData=NULL, seriesMarkers=NULL, seriesOptions=NULL, seriesPriceLines=NULL, seriesTypes=NULL, timeRangeVisibleLogicalRange=NULL, timeRangeVisibleRange=NULL, timeScaleHeight=NULL, timeScaleWidth=NULL, width=NULL) {
    
    props <- list(id=id, chartOptions=chartOptions, click=click, crosshair=crosshair, fullChartOptions=fullChartOptions, fullPriceScaleOptions=fullPriceScaleOptions, fullSeriesOptions=fullSeriesOptions, fullTimeScaleOptions=fullTimeScaleOptions, height=height, priceScaleWidth=priceScaleWidth, seriesData=seriesData, seriesMarkers=seriesMarkers, seriesOptions=seriesOptions, seriesPriceLines=seriesPriceLines, seriesTypes=seriesTypes, timeRangeVisibleLogicalRange=timeRangeVisibleLogicalRange, timeRangeVisibleRange=timeRangeVisibleRange, timeScaleHeight=timeScaleHeight, timeScaleWidth=timeScaleWidth, width=width)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Tvlwc',
        namespace = 'dash_tvlwc',
        propNames = c('id', 'chartOptions', 'click', 'crosshair', 'fullChartOptions', 'fullPriceScaleOptions', 'fullSeriesOptions', 'fullTimeScaleOptions', 'height', 'priceScaleWidth', 'seriesData', 'seriesMarkers', 'seriesOptions', 'seriesPriceLines', 'seriesTypes', 'timeRangeVisibleLogicalRange', 'timeRangeVisibleRange', 'timeScaleHeight', 'timeScaleWidth', 'width'),
        package = 'dashTvlwc'
        )

    structure(component, class = c('dash_component', 'list'))
}
