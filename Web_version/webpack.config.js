const path = require('path');
// settings = require('./settings');

module.exports = {
  entry: {
    App: "./app/assets/js/scripts.js"
  },
  output: {
    path: path.resolve(__dirname, "./app/temp/scripts"),
    filename: "app-bundled.js"
  },
  target: 'node',
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      }
    ]
  },
  mode: 'development'
}