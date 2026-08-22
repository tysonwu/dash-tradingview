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
