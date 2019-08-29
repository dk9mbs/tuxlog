import Vue from 'vue'
import App from './App.vue'

import VueRouter from 'vue-router';
Vue.use(VueRouter);

import VueSidebarMenu from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
Vue.use(VueSidebarMenu)


export const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [
    { path: '/', component: {template: '<div>home</div>'} },
    { path: '/about', component: {template: '<div>about</div>'} },
    { path: '/contact', component: {template: '<div>contact</div>'} },
    { path: '/qso', component: App }
    ]
  });


//Vue.config.productionTip = false

//new Vue({
//  render: h => h(App),
//}).$mount('#app')



new Vue({
  router,
  data() { return {
    menu: [
      {
          href: '/',
          title: 'Dashboard',
          icon: 'fa fa-user'
      },
      {
          href: '#',
          title: 'Charts',
          icon: 'fa fa-chart-area'
      },
  ]
  }
  },
  template: `
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#">tuxlog</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="#">dk9mbs.de</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown text="Log" right>
        <b-dropdown-item href="#"><router-link to="/qso">Log QSO</router-link></b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown text="Help" right>
        <b-dropdown-item href="#"><router-link to="/about">About</router-link></b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown text="Lang" right>
          <b-dropdown-item href="#">DE</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown right>
          <template slot="button-content"><em>User</em></template>
          <b-dropdown-item href="#">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>

  <sidebar-menu :menu="menu" />
    <router-view class="view"></router-view>
  </div>
`
}).$mount('#app');
