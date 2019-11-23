/* https://cli.vuejs.org/guide/webpack.html#modifying-options-of-a-plugin */
module.exports = {
devServer: {
    proxy: 'http://localhost:5000',
  },
  configureWebpack: {
    resolve: {
    alias: {
	'vue$': 'vue/dist/vue.esm.js'
    }
  }
 },
 publicPath: "tuxlog/"
}
