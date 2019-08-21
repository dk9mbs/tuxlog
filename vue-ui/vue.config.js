/* https://cli.vuejs.org/guide/webpack.html#modifying-options-of-a-plugin */
module.exports = {
  configureWebpack: {
    resolve: {
    alias: {
	'vue$': 'vue/dist/vue.esm.js'
    }
  }
 }
}
