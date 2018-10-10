const VueLoaderPlugin = require('vue-loader/lib/plugin');
const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const webpack = require('webpack');


module.exports = (env, argv) => {

    const isProduction = argv && argv.mode === 'production';
    return {
        entry: {
            main: [
                path.resolve('./ziscz/assets/main.js') // dynamic and async component import
            ],
        },
        output: {
            path: path.resolve('./ziscz/static/build/'),
            filename: isProduction ? "[name].[hash].js" : "[name].js",
            chunkFilename: 'bundle.[name].[chunkhash].js',
            publicPath: '/static/build/',
        },

        module: {
            rules: [
                /*{
                    test: /\.(png|jpg|gif|svg)$/i,
                    use: [
                        {
                            loader: 'url-loader',
                            options: {
                                limit: 20 * 1024
                            }
                        }
                    ]
                },*/
                {
                    test: /\.(png|jpg|gif|eot|svg|ttf|woff|woff2)$/,
                    use: [
                        {
                            loader: 'file-loader',
                            options: {}
                        }
                    ]
                },
                {
                    test: /\.vue$/,
                    loader: 'vue-loader'
                },
                {
                    test: /\.js$/,
                    loader: 'babel-loader',
                    // exclude: /node_modules/,
                },
                {
                    test: /\.(s?css)$/,
                    use: [
                        {
                            loader: 'vue-style-loader', // inject CSS to page
                        },
                        {
                            loader: 'css-loader', // translates CSS into CommonJS modules
                        },
                        {
                            loader: 'postcss-loader', // Run post css actions
                            options: {
                                plugins: function () { // post css plugins, can be exported to postcss.config.js
                                    return [
                                        require('precss'),
                                        require('autoprefixer')
                                    ];
                                }
                            }
                        },
                        {
                            loader: 'sass-loader', // compiles Sass to CSS
                            options: {
                                // language=SCSS
                                data: '@import "ziscz/assets/scss/variables";'
                            }
                        }
                    ]
                },
            ]
        },
        devServer: {
            headers: {
                "Access-Control-Allow-Origin": "\*"
            },
            //hot: true,
            inline: true,
            compress: true,
            overlay: {warnings: false, errors: true},
            proxy: {
                '*': 'http://localhost:8000'
            }
        },
        resolve: {
            alias: {
                'vue$': 'vue/dist/vue.esm.js',
            },
            extensions: ['*', '.js', '.vue', '.json']
        },
        optimization: {
            splitChunks: {
                //chunks: 'all'
            },
        },

        plugins: [
            new VueLoaderPlugin(),
            new BundleTracker({filename: './ziscz/webpack-stats.json'}),
        ]
    }
};