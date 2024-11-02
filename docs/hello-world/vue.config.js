const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    client: {
      webSocketURL: 'auto://0.0.0.0:8080/ws'
    }
  },
  publicPath: '/DCode/'
})
