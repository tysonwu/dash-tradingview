# AUTO GENERATED FILE - DO NOT EDIT

#' @export
tvlwc <- function(id=NULL, label=NULL, value=NULL) {
    
    props <- list(id=id, label=label, value=value)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Tvlwc',
        namespace = 'dash_tvlwc',
        propNames = c('id', 'label', 'value'),
        package = 'dashTvlwc'
        )

    structure(component, class = c('dash_component', 'list'))
}
