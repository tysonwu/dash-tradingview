# AUTO GENERATED FILE - DO NOT EDIT

#' @export
tvlwo <- function(id=NULL, barsInLogicalRange=NULL, chartOptions=NULL, click=NULL, crosshair=NULL, crosshairPosition=NULL, dataAction=NULL, dataResult=NULL, dblClick=NULL, fullChartOptions=NULL, fullPriceScaleOptions=NULL, fullSeriesOptions=NULL, fullTimeScaleOptions=NULL, height=NULL, paneOptions=NULL, priceScaleWidth=NULL, reportThrottle=NULL, screenshot=NULL, screenshotRequest=NULL, series=NULL, subscribeClick=NULL, subscribeCrosshair=NULL, subscribeDblClick=NULL, subscribeSize=NULL, subscribeVisibleRange=NULL, tick=NULL, timeScaleAction=NULL, timeScaleHeight=NULL, timeScaleWidth=NULL, visibleLogicalRange=NULL, visibleRange=NULL, watermark=NULL, width=NULL) {
    
    props <- list(id=id, barsInLogicalRange=barsInLogicalRange, chartOptions=chartOptions, click=click, crosshair=crosshair, crosshairPosition=crosshairPosition, dataAction=dataAction, dataResult=dataResult, dblClick=dblClick, fullChartOptions=fullChartOptions, fullPriceScaleOptions=fullPriceScaleOptions, fullSeriesOptions=fullSeriesOptions, fullTimeScaleOptions=fullTimeScaleOptions, height=height, paneOptions=paneOptions, priceScaleWidth=priceScaleWidth, reportThrottle=reportThrottle, screenshot=screenshot, screenshotRequest=screenshotRequest, series=series, subscribeClick=subscribeClick, subscribeCrosshair=subscribeCrosshair, subscribeDblClick=subscribeDblClick, subscribeSize=subscribeSize, subscribeVisibleRange=subscribeVisibleRange, tick=tick, timeScaleAction=timeScaleAction, timeScaleHeight=timeScaleHeight, timeScaleWidth=timeScaleWidth, visibleLogicalRange=visibleLogicalRange, visibleRange=visibleRange, watermark=watermark, width=width)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Tvlwo',
        namespace = 'dash_tvlwc',
        propNames = c('id', 'barsInLogicalRange', 'chartOptions', 'click', 'crosshair', 'crosshairPosition', 'dataAction', 'dataResult', 'dblClick', 'fullChartOptions', 'fullPriceScaleOptions', 'fullSeriesOptions', 'fullTimeScaleOptions', 'height', 'paneOptions', 'priceScaleWidth', 'reportThrottle', 'screenshot', 'screenshotRequest', 'series', 'subscribeClick', 'subscribeCrosshair', 'subscribeDblClick', 'subscribeSize', 'subscribeVisibleRange', 'tick', 'timeScaleAction', 'timeScaleHeight', 'timeScaleWidth', 'visibleLogicalRange', 'visibleRange', 'watermark', 'width'),
        package = 'dashTvlwc'
        )

    structure(component, class = c('dash_component', 'list'))
}
