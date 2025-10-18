const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: './',  // 确保使用相对路径加载资源
  chainWebpack: config => {
    config.plugin('define').tap(args => {
      args[0]['__VUE_PROD_HYDRATION_MISMATCH_DETAILS__'] = true;
      return args;
    });
  },
});