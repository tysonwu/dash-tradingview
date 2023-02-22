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

    const chartContainerRef = useRef();
    const tvChart = useRef(null);

    function handleChartOptions(chartOptions) {
        // function to evaluate js string given from user to function if there is any
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

    useEffect(
        () => {
            tvChart.current = createChart(chartContainerRef.current, handleChartOptions(chartOptions));

            const handleResize = () => {
                tvChart.current.applyOptions(
                    { width: chartContainerRef.current.clientWidth, height: chartContainerRef.current.clientHeight }
                );
            };
            window.addEventListener('resize', handleResize);

            tvChart.current.timeScale().fitContent();

            // keep track of all series on chart seriesId => seriesApi
            const allSeries = new Map();
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
                allSeries.set(seriesId, series);
            };

            function handleMouseEvent(param) {
                // match index key (seriesId) to the param by joining through seriesApi
                param.seriesPrices = Object.fromEntries([...allSeries].map(([seriesId, seriesApi]) => [seriesId, param.seriesPrices.get(seriesApi)]));
                return param;
            };

            tvChart.current.subscribeCrosshairMove((param) => { setProps({ crosshair: handleMouseEvent(param) }) });
            tvChart.current.subscribeClick((param) => { setProps({ click: handleMouseEvent(param) }) });

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
                // get the seriesApi.option() in each of the seriesApi in allSeries; with seriesId (in allSeries) as key
                fullSeriesOptions: Object.fromEntries([...allSeries].map(([seriesId, seriesApi]) => [seriesId, seriesApi.options()])),
                fullTimeScaleOptions: tvChart.current.timeScale().options(),
            })

            return () => {
                window.removeEventListener('resize', handleResize);
                tvChart.current.remove();
            };
        },
        [
            setProps,
            chartOptions,
            seriesData,
            seriesTypes,
            seriesOptions,
            seriesMarkers,
            seriesPriceLines,
            width,
            height,
        ]
    );

    return (
        <div id={id} ref={chartContainerRef} style={{ height: height, width: width }} />
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