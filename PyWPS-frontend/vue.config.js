const {defineConfig} = require('@vue/cli-service')

module.exports = defineConfig({
    transpileDependencies: true,
    lintOnSave: false,
    devServer: {
        client: {
            overlay: false
        },
        proxy: {
            '/api': {
                target: 'http://10.191.243.20:5555/', // 确保目标 URL 是正确的，并且以斜杠 '/' 结尾
                changeOrigin: true, // 支持虚拟托管的站点
                pathRewrite: {'^/api': ''}, // 重写路径，移除请求中的 '/api' 部分
            },
        },
    }
})