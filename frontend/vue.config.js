const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: './',
  chainWebpack: config => {
    config.plugin('define').tap(args => {
      args[0]['__VUE_PROD_HYDRATION_MISMATCH_DETAILS__'] = true;
      return args;
    });
  },
  devServer: {
    hot: true,                // 开启热更新
    open: false,               // 自动打开浏览器
    historyApiFallback: true, // 防止404错误
    client: {
      overlay: {
        errors: true,         // 显示错误
        warnings: false,      // 不显示警告
      },
    },
  },
});
