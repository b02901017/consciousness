const path = require('path');
const webpack = require('webpack');
const loaders = require('./webpack.loader');

module.exports = {
    devtool: 'cheap-module-eval-source-map',
    entry: ['babel-polyfill', 'whatwg-fetch', './src/index'],
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'bundle.js',
        publicPath: '/static/',
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify('development'),
            },
        }),
    ],
    module: {
        loaders : loaders

    },
};
