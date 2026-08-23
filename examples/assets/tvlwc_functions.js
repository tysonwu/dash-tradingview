/* Formatter functions the charts refer to by name.
 *
 * Options that must be JavaScript functions cannot cross the Python boundary,
 * so they are registered here and named as strings from Python:
 *
 *     chartOptions={'localization': {'priceFormatter': 'usd'}}
 */
window.dashTvlwcFunctions = window.dashTvlwcFunctions || {};

window.dashTvlwcFunctions.usd = function (price) {
    return '$' + price.toFixed(2);
};

window.dashTvlwcFunctions.compact = function (value) {
    if (value >= 1e6) { return (value / 1e6).toFixed(1) + 'M'; }
    if (value >= 1e3) { return (value / 1e3).toFixed(1) + 'k'; }
    return value.toFixed(0);
};

/* Maturity labels for the yield curve chart. Registered against
 * `localization.timeFormatter`, which is what the yield curve scale actually
 * calls; it receives the maturity in `baseResolution` units, default months.
 *
 * Spelt deliberately unlike the library's own `6M` / `10Y` defaults, so the
 * axis makes it obvious whether this function is being called at all. */
window.dashTvlwcFunctions.maturity = function (months) {
    if (months < 12) { return months + ' mo'; }
    var years = months / 12;
    return (years % 1 === 0 ? years : years.toFixed(1)) + ' yr';
};

/* Strike labels for the options chart, whose horizontal axis is a price. */
window.dashTvlwcFunctions.strike = function (price) {
    return price.toFixed(0);
};
