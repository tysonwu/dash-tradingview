# AUTO GENERATED FILE - DO NOT EDIT

#' @export
tvlwc <- function(id=NULL, chartOptions=NULL, click=NULL, crosshair=NULL, fullChartOptions=NULL, fullPriceScaleOptions=NULL, fullSeriesOptions=NULL, fullTimeScaleOptions=NULL, height=NULL, priceScaleWidth=NULL, reportThrottle=NULL, series=NULL, subscribeClick=NULL, subscribeCrosshair=NULL, subscribeSize=NULL, subscribeVisibleRange=NULL, timeScaleHeight=NULL, timeScaleWidth=NULL, visibleLogicalRange=NULL, visibleRange=NULL, width=NULL) {
    
    props <- list(id=id, chartOptions=chartOptions, click=click, crosshair=crosshair, fullChartOptions=fullChartOptions, fullPriceScaleOptions=fullPriceScaleOptions, fullSeriesOptions=fullSeriesOptions, fullTimeScaleOptions=fullTimeScaleOptions, height=height, priceScaleWidth=priceScaleWidth, reportThrottle=reportThrottle, series=series, subscribeClick=subscribeClick, subscribeCrosshair=subscribeCrosshair, subscribeSize=subscribeSize, subscribeVisibleRange=subscribeVisibleRange, timeScaleHeight=timeScaleHeight, timeScaleWidth=timeScaleWidth, visibleLogicalRange=visibleLogicalRange, visibleRange=visibleRange, width=width)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Tvlwc',
        namespace = 'dash_tvlwc',
        propNames = c('id', 'chartOptions', 'click', 'crosshair', 'fullChartOptions', 'fullPriceScaleOptions', 'fullSeriesOptions', 'fullTimeScaleOptions', 'height', 'priceScaleWidth', 'reportThrottle', 'series', 'subscribeClick', 'subscribeCrosshair', 'subscribeSize', 'subscribeVisibleRange', 'timeScaleHeight', 'timeScaleWidth', 'visibleLogicalRange', 'visibleRange', 'width'),
        package = 'dashTvlwc'
        )

    structure(component, class = c('dash_component', 'list'))
}
