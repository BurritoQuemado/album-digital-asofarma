import path from 'path'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'
import OptimizeCSSAssetsPlugin from 'optimize-css-assets-webpack-plugin'
import BundleTracker from 'webpack-bundle-tracker'
import UglifyJSPlugin from 'uglifyjs-webpack-plugin'
import postcssFocus from 'postcss-focus'
import rucksack from 'rucksack-css'
import lost from 'lost'
import autoprefixer from 'autoprefixer'
import precss from 'precss'
import base from './config.base.babel'

module.exports = base({
    mode: 'production',
    devtool: 'hidden-source-map',
    output: {
        path: path.resolve(__dirname, '..', 'dist'),
        filename: '[name]-[hash].js',
        publicPath: '/static/',
    },
    optimization: {
        minimizer: [
            new UglifyJSPlugin({
                sourceMap: true,
                uglifyOptions: {
                    output: {
                        comments: false,
                    },
                    compress: {
                        drop_console: true,
                    },
                },
            }),
            new OptimizeCSSAssetsPlugin({}),
        ],
    },
    // In production, we skip all hot-reloading stuff
    entry: {
        main: [
            'babel-polyfill',
            path.join(__dirname, '..', 'src/main.js'), // Start with js/app.js
        ],
    },
    // We use ExtractTextPlugin so we get a seperate CSS file instead
    // of the CSS being in the JS and injected as a style tag
    cssLoaders: [
        MiniCssExtractPlugin.loader,
        'css-loader',
    ],
    // Load Stylus with SourceMaps
    stylusLoaders: [
        MiniCssExtractPlugin.loader,
        {
            loader: 'css-loader',
            options: {
                importLoaders: 2,
                sourceMap: true,
                localIdentName: '[local]___[hash:base64:10]',
            },
        },
        'stylus-loader',
    ],
    sassLoaders: [
        MiniCssExtractPlugin.loader,
        {
            loader: 'css-loader', // translates CSS into CommonJS modules
        }, {
            loader: 'postcss-loader', // Run post css actions
            options: {
                plugins: () => { // post css plugins, can be exported to postcss.config.js
                    return [
                        precss,
                        autoprefixer,
                    ]
                },
            },
        }, {
            loader: 'sass-loader',
        },
    ],
    // In production, we minify our CSS with cssnano
    stylusPlugins: [
        lost(),
        postcssFocus(), // Add a :focus to every :hover
        rucksack({
            autoprefixer: true,
            fallbacks: true,
        }),
    ],
    plugins: [
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // both options are optional
            filename: '[name]-[hash].css',
            allChunks: true,
        }),
        // Set the process.env to production so React includes the production
        // version of itself
        new BundleTracker({ filename: '../webpack-stats-prod.json' }),
    ],
})
