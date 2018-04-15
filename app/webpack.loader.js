const loaders = [
    {
        test: /\.js$/,
        loaders: ['babel-loader'],
        exclude: /node_modules\/(?!material-ui\/)/,
    },
    {
        test: /\.css$/,
        loader: 'style-loader!css-loader?minimize=true',
    },
    {
        test: /\.png$/,
        loader: 'url-loader?limit=100000'
    },
    {
        test: /\.jpg$/,
        loader: 'file-loader'
    },
    {
        test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url-loader?limit=10000&mimetype=application/font-woff'
    },
    {
        test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url-loader?limit=10000&mimetype=application/octet-stream'
    },
    {
        test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'file-loader'
    },
    {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url-loader?limit=10000&mimetype=image/svg+xml'
    }
];

module.exports = loaders;
