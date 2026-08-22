// Vendored from dash/dash-renderer/jsx-runtime-external.js (Dash 4.4.1).
//
// Shared webpack external for react/jsx-runtime and react/jsx-dev-runtime.
// Dash provides window.ReactJSXRuntime backed by the React version loaded on
// the page; the inline fallback below rebuilds an equivalent runtime from
// window.React.createElement (and caches it on window.ReactJSXRuntime) so this
// bundle also works on Dash versions that never define the global.
//
// Upstream requires this implementation to stay in sync with dash-renderer's
// src/react-shim.js. Re-check it on each Dash major upgrade.
const jsxRuntimeExternal = `var (window.ReactJSXRuntime || (window.ReactJSXRuntime = (function (React) {
    function jsx(type, config, maybeKey) {
        var props = {};
        var children = null;
        if (config != null) {
            if (config.key !== undefined) {
                props.key = '' + config.key;
            }
            for (var propName in config) {
                if (
                    Object.prototype.hasOwnProperty.call(config, propName) &&
                    propName !== 'key' &&
                    propName !== '__self' &&
                    propName !== '__source'
                ) {
                    if (propName === 'children') {
                        children = config[propName];
                    } else {
                        props[propName] = config[propName];
                    }
                }
            }
        }
        if (maybeKey !== undefined) {
            props.key = '' + maybeKey;
        }
        if (children === null || children === undefined) {
            return React.createElement(type, props);
        }
        return Array.isArray(children)
            ? React.createElement.apply(React, [type, props].concat(children))
            : React.createElement(type, props, children);
    }
    return {jsx: jsx, jsxs: jsx, jsxDEV: jsx, Fragment: React.Fragment};
})(window.React)))`;

module.exports = {jsxRuntimeExternal};
