# AUTO GENERATED FILE - DO NOT EDIT

#' @export
tvlwc <- function(id=NULL, chartOptions=NULL, height=NULL, width=NULL) {
    
    props <- list(id=id, chartOptions=chartOptions, height=height, width=width)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Tvlwc',
        namespace = 'dash_tvlwc',
        propNames = c('id', 'chartOptions', 'height', 'width'),
        package = 'dashTvlwc'
        )

    structure(component, class = c('dash_component', 'list'))
}
