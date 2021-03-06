const { InjectManifest } = require('workbox-webpack-plugin');

module.exports = {
  lintOnSave: process.env.NODE_ENV !== 'production',
  transpileDependencies: [
    'vuetify',
  ],
  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args => {
        args[0].title = 'Bilolok'
        return args
      })
  },
  configureWebpack: {
    plugins: [
      new InjectManifest({
        swSrc: './src/service-worker-base.js',
        swDest: 'service-worker.js',
      }),
    ],
  },
};
