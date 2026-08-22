const path = require('path');
const WebpackDashDynamicImport = require('@plotly/webpack-dash-dynamic-import');
const packagejson = require('./package.json');
const {jsxRuntimeExternal} = require('./jsx-runtime-external');

const dashLibraryName = packagejson.name.replace(/-/g, '_');

module.exports = (env, argv) => {
    const overrides = module.exports || {};

    let mode;
    if (argv && argv.mode) {
        mode = argv.mode;
    } else if (overrides.mode) {
        mode = overrides.mode;
    } else {
        mode = 'production';
    }

    let filename = (overrides.output || {}).filename;
    if (!filename) {
        const modeSuffix = mode === 'development' ? 'dev' : 'min';
        filename = `${dashLibraryName}.${modeSuffix}.js`;
    }

    const entry = overrides.entry || {main: './src/lib/index.ts'};

    // `devtool` alone emits the .map files. The upstream boilerplate pairs it
    // with SourceMapDevToolPlugin; under webpack 5 the two mechanisms collide
    // on the same output filename, so only one is used here.
    const devtool = overrides.devtool || 'source-map';

    const externals =
        'externals' in overrides
            ? overrides.externals
            : {
                  react: 'React',
                  'react-dom': 'ReactDOM',
                  'react/jsx-runtime': jsxRuntimeExternal,
                  'react/jsx-dev-runtime': jsxRuntimeExternal,
                  'prop-types': 'PropTypes',
              };

    return {
        mode,
        entry,
        output: {
            path: path.resolve(__dirname, dashLibraryName),
            chunkFilename: '[name].js',
            filename,
            library: {
                name: dashLibraryName,
                type: 'window',
            },
        },
        devtool,
        devServer: {
            static: {
                directory: path.join(__dirname, '/'),
            },
        },
        externals,
        resolve: {
            extensions: ['.tsx', '.ts', '.jsx', '.js'],
        },
        module: {
            rules: [
                {
                    test: /\.[jt]sx?$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                    },
                },
                {
                    test: /\.css$/,
                    use: [{loader: 'style-loader'}, {loader: 'css-loader'}],
                },
            ],
        },
        optimization: {
            splitChunks: {
                name: '[name].js',
                cacheGroups: {
                    async: {
                        chunks: 'async',
                        minSize: 0,
                        name(module, chunks, cacheGroupKey) {
                            return `${cacheGroupKey}-${chunks[0].name}`;
                        },
                    },
                    shared: {
                        chunks: 'all',
                        minSize: 0,
                        minChunks: 2,
                        name: `${dashLibraryName}-shared`,
                    },
                },
            },
        },
        plugins: [new WebpackDashDynamicImport()],
    };
};
