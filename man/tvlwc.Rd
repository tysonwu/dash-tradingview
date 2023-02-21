% Auto-generated: do not edit by hand
\name{tvlwc}

\alias{tvlwc}

\title{Tvlwc component}

\description{
Tradingview Lightweight Chart object
}

\usage{
tvlwc(id=NULL, chartOptions=NULL, click=NULL, crosshair=NULL,
fullChartOptions=NULL, fullPriceScaleOptions=NULL,
fullSeriesOptions=NULL, fullTimeScaleOptions=NULL,
height=NULL, priceScaleWidth=NULL, seriesData=NULL,
seriesMarkers=NULL, seriesOptions=NULL,
seriesPriceLines=NULL, seriesTypes=NULL,
timeRangeVisibleLogicalRange=NULL,
timeRangeVisibleRange=NULL, timeScaleHeight=NULL,
timeScaleWidth=NULL, width=NULL)
}

\arguments{
\item{id}{Character. The ID of this component}

\item{chartOptions}{Named list. Object containing all chart options
See https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions for possible options}

\item{click}{Named list. Last-clicked on chart coordinates; read-only}

\item{crosshair}{Named list. Crosshair coordinates; read-only}

\item{fullChartOptions}{Named list. Full chart options including defaults; read-only}

\item{fullPriceScaleOptions}{Named list. Full chart price scale options including defaults; read-only}

\item{fullSeriesOptions}{List of named lists. Full series options including defaults; read-only}

\item{fullTimeScaleOptions}{Named list. Full time scale options including defaults; read-only}

\item{height}{Character | numeric. Sets height of the parent div of the chart}

\item{priceScaleWidth}{Numeric. Width of price scale; read-only}

\item{seriesData}{List of list of named listss. Data for the series}

\item{seriesMarkers}{List of list of named listss. Additional markers for the series}

\item{seriesOptions}{List of named lists. Options for the series}

\item{seriesPriceLines}{List of list of named listss. Additional price lines for the series}

\item{seriesTypes}{List of a value equal to: 'bar', 'candlestick', 'area', 'baseline', 'line', 'histogram's. Type of the series}

\item{timeRangeVisibleLogicalRange}{Named list. Visible logical range; read-only}

\item{timeRangeVisibleRange}{Named list. Visible time range; read-only}

\item{timeScaleHeight}{Numeric. Height of time scale; read-only}

\item{timeScaleWidth}{Numeric. Width of time scale; read-only}

\item{width}{Character | numeric. Sets width of the parent div of the chart}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

