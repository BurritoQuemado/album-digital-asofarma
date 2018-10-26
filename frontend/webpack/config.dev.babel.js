import path from 'path'
import BundleTracker from 'webpack-bundle-tracker'

// PostCSS plugins
import postcssFocus from 'postcss-focus'
import rucksack from 'rucksack-css'
import lost from 'lost'
import autoprefixer from 'autoprefixer'
import precss from 'precss'
import base from './config.base.babel'

module.exports = base({
    mode: 'development',
    devtool: 'cheap-module-source-map',
    output: {
        path: path.resolve('../assets/bundles/'),
        filename: '[name]-[hash].js',
        publicPath: 'http://localhost:3000/assets/bundles/', // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name
    },
    // Add hot reloading in development
    entry: {
        main: [
            'babel-polyfill',
            path.join(__dirname, '..', 'src/main.js'), // Start with js/app.js
        ],
    },
    // Load the CSS in a style tag in development
    cssLoaders: [{
        loader: 'style-loader',
    }, {
        loader: 'css-loader',
        options: {
            importLoaders: 1,
            sourceMap: true,
        },
    }],
    // Load Stylus with SourceMaps
    stylusLoaders: [{
        loader: 'style-loader',
    }, {
        loader: 'css-loader',
        options: {
            importLoaders: 1,
            sourceMap: true,
            localIdentName: '[local]___[hash:base64:10]',
        },
    }, {
        loader: 'stylus-loader',
    }],
    sassLoaders: [{
        loader: 'style-loader', // inject CSS to page
    }, {
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
    }],
    // Process the CSS with PostCSS
    stylusPlugins: [
        lost(),
        postcssFocus(), // Add a :focus to every :hover
        rucksack({
            autoprefixer: true,
            fallbacks: true,
        }),
    ],
    plugins: [
        new BundleTracker({ filename: '../backend/webpack-stats.json' }),
    ],
})
