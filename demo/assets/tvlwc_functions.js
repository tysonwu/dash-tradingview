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

/* Maturity labels for the yield curve chart. Registered against
 * `localization.timeFormatter`, which is what the yield curve scale calls; it
 * receives the maturity in `baseResolution` units, months by default. */
window.dashTvlwcFunctions.maturity = function (months) {
    if (months < 12) { return months + 'M'; }
    var years = months / 12;
    return (years % 1 === 0 ? years : years.toFixed(1)) + 'Y';
};
