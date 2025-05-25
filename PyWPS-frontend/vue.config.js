const { defineConfig } = require('@vue/cli-service')
const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require('path');
const webpack = require('webpack');
// CesiumJS源代码的路径
const cesiumSource = 'node_modules/cesium/Source';
const cesiumWorkers = '../Build/Cesium/Workers';

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    output: {
      sourcePrefix: ''
    },
    resolve: {
      fallback: { "https": false, "zlib": false, "http": false, "url": false },
    },
    plugins: [
      // 复制Cesium的Assets、Widgets和Workers到一个静态目录
      new CopyWebpackPlugin({
        patterns: [
          { from: path.join(cesiumSource, cesiumWorkers), to: 'Workers' },
          { from: path.join(cesiumSource, 'Assets'), to: 'Assets' },
          { from: path.join(cesiumSource, 'Widgets'), to: 'Widgets' },
          { from: path.join(cesiumSource, 'ThirdParty'), to: 'ThirdParty' }
        ]
      }),
      new webpack.DefinePlugin({
        //在Cesium中定义一个相对基本路径来加载资源
        CESIUM_BASE_URL: JSON.stringify('')
      })
    ],
  },
  lintOnSave: false,
  devServer: {
    client: {
      overlay: false
    },
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/', // 确保目标 URL 是正确的，并且以斜杠 '/' 结尾
        changeOrigin: true, // 支持虚拟托管的站点
      },
      '/processes': {
        target: 'http://127.0.0.1:5000/', // 确保目标 URL 是正确的，并且以斜杠 '/' 结尾
        changeOrigin: true, // 支持虚拟托管的站点
      },
      '/jobs': {
        target: 'http://127.0.0.1:5000/', // 确保目标 URL 是正确的，并且以斜杠 '/' 结尾
        changeOrigin: true, // 支持虚拟托管的站点
      },
    },
  }
})


