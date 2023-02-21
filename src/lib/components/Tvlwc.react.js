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

    useEffect(
        () => {
            if ('localization' in chartOptions) {
                if ('priceFormatter' in chartOptions.localization) {
                    chartOptions.localization.priceFormatter = eval(chartOptions.localization.priceFormatter);
                }
                if ('timeFormatter' in chartOptions.localization) {
                    chartOptions.localization.timeFormatter = eval(chartOptions.localization.timeFormatter);
                }
            }
            const chart = createChart(chartContainerRef.current, chartOptions);

            const handleResize = () => {
                chart.applyOptions({ width: chartContainerRef.current.clientWidth });
            };
            chart.timeScale().fitContent();

            // keep track of all series on chart
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
                        series = chart.addBarSeries(options);
                        break;
                    case 'candlestick':
                        series = chart.addCandlestickSeries(options);
                        break;
                    case 'area':
                        series = chart.addAreaSeries(options);
                        break;
                    case 'baseline':
                        series = chart.addBaselineSeries(options);
                        break;
                    case 'line':
                        series = chart.addLineSeries(options);
                        break;
                    case 'histogram':
                        series = chart.addHistogramSeries(options);
                        break;
                    default:
                        break;
                    }
                series.setData(data);
                series.setMarkers(markers);
                for (const pl of priceLines) { series.createPriceLine(pl); }
                allSeries.set(series, seriesId);
            };
            window.addEventListener('resize', handleResize);

            // remove the param key as ISeriesApi is not serializable
            function handleMouseEvent(param) {
                const seriesPricesMerge = {}
                for (const [seriesApi, seriesPrice] of param.seriesPrices) {
                    seriesPricesMerge[allSeries.get(seriesApi)] = seriesPrice
                }
                param.seriesPrices = seriesPricesMerge;
                return param;
            };

            chart.subscribeCrosshairMove((param) => { setProps({ crosshair: handleMouseEvent(param) }) });
            chart.subscribeClick((param) => { setProps({ click: handleMouseEvent(param) }) });

            // subscribe timeScale events
            chart.timeScale().subscribeVisibleTimeRangeChange(() => { setProps({ timeRangeVisibleRange: chart.timeScale().getVisibleRange() }) });
            chart.timeScale().subscribeVisibleLogicalRangeChange(() => { setProps({ timeRangeVisibleLogicalRange: chart.timeScale().getVisibleLogicalRange() }) });
            chart.timeScale().subscribeSizeChange(() => { setProps({ timeScaleWidth: chart.timeScale().width(), timeScaleHeight: chart.timeScale().height() }) })

            setProps({
                fullChartOptions: chart.options(),
                fullPriceScaleOptions: chart.priceScale().options(),
                priceScaleWidth: chart.priceScale().width(),
                // fullSeriesOptions: [...allSeries.keys()].map((seriesApi) => {seriesApi.options()}),
                timeRangeVisibleRange: chart.timeScale().getVisibleRange(),
                timeRangeVisibleLogicalRange: chart.timeScale().getVisibleLogicalRange(),
                timeScaleWidth: chart.timeScale().width(),
                timeScaleHeight: chart.timeScale().height(),
                fullTimeScaleOptions: chart.timeScale().options(),
            })

            return () => {
                window.removeEventListener('resize', handleResize);
                chart.remove();
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
    crosshair: null,
    click: null,
    fullChartOptions: {},
    fullPriceScaleOptions: {},
    priceScaleWidth: null,
    fullSeriesOptions: [],
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
    fullSeriesOptions: PropTypes.arrayOf(PropTypes.object),

    /**
     * Visible time range; read-only
     */
    timeRangeVisibleRange: PropTypes.object,

    /**
     * Visible logical range; read-only
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