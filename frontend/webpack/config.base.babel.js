import path from 'path'
import webpack from 'webpack'
import postcss from 'poststylus'
import rupture from 'rupture'

module.exports = options => ({
    entry: options.entry,
    output: options.output,
    devtool: options.devtool,
    mode: options.mode,
    optimization: {
        ...options.optimization,
        splitChunks: {
            cacheGroups: {
                commons: {
                    test: /[\\/]node_modules[\\/]/,
                    name: 'vendors',
                    chunks: 'all',
                },
            },
        },
    },
    module: {
        rules: [
            {
                test: /\.js$/, // Transform all .js files required somewhere with Babel
                loader: 'babel-loader',
                exclude: path.join(__dirname, '..', '/node_modules/'),
            },
            {
                test: /\.css$/,
                use: options.cssLoaders,
            },
            {
                test: /\.(scss)$/,
                use: options.sassLoaders,
            },
            {
                test: /\.styl$/,
                use: options.stylusLoaders,
            },
            {
                test: /\.jpe?g$|\.gif$|\.png$/i,
                loader: 'file-loader',
                options: {
                    name: 'content/[sha512:hash:base64:7].[ext]',
                },
            },
            {
                test: /\.svg$/,
                loader: 'url-loader',
                options: {
                    limit: '32000',
                    mimetype: 'image/svg+xml',
                    name: 'content/[sha512:hash:base64:7].[ext]',
                },
            },
            {
                test: /\.woff$/,
                loader: 'url-loader',
                options: {
                    limit: '32000',
                    mimetype: 'application/font-woff',
                    name: 'content/[sha512:hash:base64:7].[ext]',
                },
            },
            {
                test: /\.woff2$/,
                loader: 'url-loader',
                options: {
                    limit: '32000',
                    mimetype: 'application/font-woff2',
                    name: 'content/[sha512:hash:base64:7].[ext]',
                },
            },
            {
                test: /\.[ot]tf$/,
                loader: 'url-loader',
                options: {
                    limit: '32000',
                    mimetype: 'application/octet-stream',
                    name: 'content/[sha512:hash:base64:7].[ext]',
                },
            },
            {
                test: /\.eot$/,
                loader: 'url-loader',
                options: {
                    limit: '32000',
                    mimetype: 'application/vnd.ms-fontobject',
                    name: 'content/[sha512:hash:base64:7].[ext]',
                },
            },
            {
                test: /\.json$/,
                loader: 'file-loader',
                options: {
                    name: 'content/[sha512:hash:base64:7].[ext]',
                },
                exclude: path.join(__dirname, '..', '/node_modules/'),
            },
        ],
    },
    plugins: options.plugins.concat([
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            jquery: 'jquery',
        }),
        new webpack.LoaderOptionsPlugin({
            test: /\.styl$/,
            stylus: {
                default: {
                    use: [
                        postcss(options.stylusPlugins),
                        rupture(),
                    ],
                },
            },
        }),
    ]),
    resolve: {
        extensions: ['.js', '.styl', '.css', '.scss'],
        modules: [path.join(__dirname, '..', 'src'), 'node_modules'],
        alias: {
            src: path.resolve(__dirname, '../src'),
            assets: path.resolve(__dirname, '../src/assets'),
        },
    },
    target: 'web', // Make web variables accessible to webpack, e.g. window
    performance: options.performance || {},
})
