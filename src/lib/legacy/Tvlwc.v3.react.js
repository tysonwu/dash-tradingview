import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { createChart } from 'lightweight-charts';


/**
 * Tradingview Lightweight Chart object
 */

const Tvlwc = props => {

    const {
        id,
        setProps,
        chartOptions,
        seriesData,
        seriesTypes,
        seriesOptions,
        seriesMarkers,
        seriesPriceLines,
        width,
        height,
    } = props;

    const chartContainerRef = useRef(null);
    const tvChart = useRef(null);

    // keep track of all series on chart seriesId => seriesApi
    const allSeries = useRef(new Map());

    function handleChartOptions(chartOptions) {
        if ('localization' in chartOptions) {
            if ('priceFormatter' in chartOptions.localization) {
                chartOptions.localization.priceFormatter = eval(chartOptions.localization.priceFormatter);
            }
            if ('timeFormatter' in chartOptions.localization) {
                chartOptions.localization.timeFormatter = eval(chartOptions.localization.timeFormatter);
            }
        };
        return chartOptions;
    };

    function handleMouseEvent(param) {
        // match index key (seriesId) to the param by joining through seriesApi
        param.seriesPrices = Object.fromEntries([...allSeries.current].map(([seriesId, seriesApi]) => [seriesId, param.seriesPrices.get(seriesApi)]));
        return param;
    };

    const handleResize = () => {
        tvChart.current.applyOptions({ width: chartContainerRef.current.clientWidth, height: chartContainerRef.current.clientHeight });
    };

    useEffect(
        () => {
            return () => {
                tvChart.current.remove();
                window.removeEventListener('resize', handleResize);
            };
        },
        [chartContainerRef]
    )

    useEffect(
        () => {
            if (tvChart.current) {
                // tvChart already exists and just apply chart options
                tvChart.current.applyOptions(handleChartOptions(chartOptions));
            } else {
                // tvChart is null, so create one (probably first init)
                tvChart.current = createChart(chartContainerRef.current, handleChartOptions(chartOptions));
                window.addEventListener('resize', handleResize);
                tvChart.current.timeScale().fitContent();
                // update the height and width once upon init
                handleResize();
                tvChart.current.subscribeCrosshairMove((param) => { setProps({ crosshair: handleMouseEvent(param) }) });
                tvChart.current.subscribeClick((param) => { setProps({ click: handleMouseEvent(param) }) });
            }

            // subscribe timeScale events
            tvChart.current.timeScale().subscribeVisibleTimeRangeChange(() => {
                setProps({ timeRangeVisibleRange: tvChart.current.timeScale().getVisibleRange() })
            });
            tvChart.current.timeScale().subscribeVisibleLogicalRangeChange(() => {
                setProps({ timeRangeVisibleLogicalRange: tvChart.current.timeScale().getVisibleLogicalRange() })
            });
            tvChart.current.timeScale().subscribeSizeChange(() => {
                setProps({ timeScaleWidth: tvChart.current.timeScale().width(), timeScaleHeight: tvChart.current.timeScale().height() })
            });

            setProps({
                fullChartOptions: tvChart.current.options(),
                fullPriceScaleOptions: tvChart.current.priceScale().options(),
                priceScaleWidth: tvChart.current.priceScale().width(),
                fullTimeScaleOptions: tvChart.current.timeScale().options(),
            });
        },
        [
            setProps,
            chartOptions,
            width,
            height
        ]
    );

    useEffect(
        () => {
            if (tvChart.current) {
                const newSeries = new Map();
                for (var i = 0; i < seriesData.length; i++) {
                    var series, options, data, markers, priceLines, seriesId;
                    options = seriesOptions[i] ? seriesOptions[i] : {};
                    data = seriesData[i] ? seriesData[i] : [];
                    markers = seriesMarkers[i] ? seriesMarkers[i] : [];
                    priceLines = seriesPriceLines[i] ? seriesPriceLines[i] : [];
                    seriesId = i;

                    switch (seriesTypes[i]) {
                        case 'bar':
                            series = tvChart.current.addBarSeries(options);
                            break;
                        case 'candlestick':
                            series = tvChart.current.addCandlestickSeries(options);
                            break;
                        case 'area':
                            series = tvChart.current.addAreaSeries(options);
                            break;
                        case 'baseline':
                            series = tvChart.current.addBaselineSeries(options);
                            break;
                        case 'line':
                            series = tvChart.current.addLineSeries(options);
                            break;
                        case 'histogram':
                            series = tvChart.current.addHistogramSeries(options);
                            break;
                        default:
                            break;
                        }
                    series.setData(data);
                    series.setMarkers(markers);
                    for (const pl of priceLines) { series.createPriceLine(pl); }
                    // add this seriesId and seriesApi pair to existing allSeries state
                    newSeries.set(seriesId, series);
                };

                allSeries.current = newSeries;

                setProps({
                    // get the seriesApi.option() in each of the seriesApi in allSeries; with seriesId (in allSeries) as key
                    fullSeriesOptions: Object.fromEntries([...allSeries.current].map(([seriesId, seriesApi]) => [seriesId, seriesApi.options()])),
                })
            }

            return () => {
                allSeries.current.forEach( (seriesApi) => {
                    tvChart.current.removeSeries(seriesApi);
                });
            };
        },
        [
            setProps,
            seriesData,
            seriesTypes,
            seriesOptions,
            seriesMarkers,
            seriesPriceLines
        ]
    );

    return (
        <div id={id} ref={chartContainerRef} style={{height: height, width: width}} />
    );
}

Tvlwc.defaultProps = {
    chartOptions: {},
    seriesData: [],
    seriesTypes: [],
    seriesOptions: [],
    seriesMarkers: [],
    seriesPriceLines: [],
    crosshair: {},
    click: {},
    fullChartOptions: {},
    fullPriceScaleOptions: {},
    priceScaleWidth: null,
    fullSeriesOptions: {},
    timeRangeVisibleRange: {},
    timeRangeVisibleLogicalRange: {},
    timeScaleWidth: null,
    timeScaleHeight: null,
    fullTimeScaleOptions: {},
    width: 600,
    height: 400,
};

Tvlwc.propTypes = {
    /**
     * The ID of this component
     */
    id: PropTypes.string,

    /**
     * Object containing all chart options
     * See https://tradingview.github.io/lightweight-charts/docs/api/interfaces/ChartOptions for possible options
     */
    chartOptions: PropTypes.object,

    /**
     * Data for the series
     */
    seriesData: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.object)),

    /**
     * Type of the series
     */
    seriesTypes: PropTypes.arrayOf(PropTypes.oneOf(['bar', 'candlestick', 'area', 'baseline', 'line', 'histogram'])),

    /**
     * Options for the series
     */
    seriesOptions: PropTypes.arrayOf(PropTypes.object),

    /**
     * Additional markers for the series
     */
    seriesMarkers: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.object)),

    /**
     * Additional price lines for the series
     */
    seriesPriceLines: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.object)),

    /**
     * Crosshair coordinates; read-only
     */
    crosshair: PropTypes.object,

    /**
     * Last-clicked on chart coordinates; read-only
     */
    click: PropTypes.object,

    /**
     * Full chart options including defaults; read-only
     */
    fullChartOptions: PropTypes.object,

    /**
     * Full chart price scale options including defaults; read-only
     */
    fullPriceScaleOptions: PropTypes.object,

    /**
     * Width of price scale; read-only
     */
    priceScaleWidth: PropTypes.number,

    /**
     * Full series options including defaults; read-only
     */
    fullSeriesOptions: PropTypes.object,

    /**
     * Visible time range (dates); read-only
     */
    timeRangeVisibleRange: PropTypes.object,

    /**
     * Visible logical range (bar numbers); read-only
     */
    timeRangeVisibleLogicalRange: PropTypes.object,

    /**
     * Width of time scale; read-only
     */
    timeScaleWidth: PropTypes.number,

    /**
     * Height of time scale; read-only
     */
    timeScaleHeight: PropTypes.number,

    /**
     * Full time scale options including defaults; read-only
     */
    fullTimeScaleOptions: PropTypes.object,

    /**
     * Sets width of the parent div of the chart
     */
    width: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),

    /**
     * Sets height of the parent div of the chart
     */
    height: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),

    /**
     * Set props
     */
    setProps: PropTypes.func,
};

export default Tvlwc;