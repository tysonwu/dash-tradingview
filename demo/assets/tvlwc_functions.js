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
