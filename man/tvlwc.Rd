% Auto-generated: do not edit by hand
\name{tvlwc}

\alias{tvlwc}

\title{Tvlwc component}

\description{
Tradingview Lightweight Chart object
}

\usage{
tvlwc(id=NULL, chartOptions=NULL, data=NULL, height=NULL,
width=NULL)
}

\arguments{
\item{id}{Character. The ID of this component}

\item{chartOptions}{Named list. Object containing all chart options
See https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions for possible options}

\item{data}{List of lists containing elements 'seriesdata', 'seriestype', 'seriesoptions', 'markers', 'pricelines'.
those elements have the following types:
  - seriesdata (list of named lists; optional)
  - seriestype (a value equal to: 'bar', 'candlestick', 'area', 'baseline', 'line', 'histogram'; optional)
  - seriesoptions (named list; optional)
  - markers (list of named lists; optional)
  - pricelines (list of named lists; optional)s. The data for the series}

\item{height}{Character | numeric. Sets height of the parent div of the chart}

\item{width}{Character | numeric. Sets width of the parent div of the chart}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

