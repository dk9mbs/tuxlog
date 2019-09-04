import Vue from 'vue'
import Qso from './components/tuxlog-qso.vue'
import Rig from './components/tuxlog-rig.vue'

import VueRouter from 'vue-router';
Vue.use(VueRouter);

import axios from 'axios'
import tuxlogInput from './components/tuxlog-input.vue'
import tuxlogOption from './components/tuxlog-option.vue'
import tuxlogCheckbox from './components/tuxlog-checkbox.vue'
import tuxlogCallHistory from './components/tuxlog-call-history.vue'
import tuxlogCallHistoryFilter from './components/tuxlog-call-history-filter.vue'
import tuxlogRigctl from './components/tuxlog-rigctl.vue'
import tuxlogMenu from './components/tuxlog-menu.vue'
import tuxlogDataView from './components/tuxlog-dataview.vue'

import { BFormInput } from 'bootstrap-vue'
import { BFormGroup } from 'bootstrap-vue'
import { BFormSelect } from 'bootstrap-vue'
import { BFormCheckboxGroup } from 'bootstrap-vue'
import { BFormCheckbox } from 'bootstrap-vue'
import { BTable } from 'bootstrap-vue'
import { BSpinner } from 'bootstrap-vue'
import { BButton } from 'bootstrap-vue'
import { BCollapse } from 'bootstrap-vue'
import { BCard } from 'bootstrap-vue'
import { BContainer } from 'bootstrap-vue'
import { BCol } from 'bootstrap-vue'
import { BRow } from 'bootstrap-vue'
import { BNavbar,BNavbarBrand,BNavbarToggle,BNavbarNav  } from 'bootstrap-vue'
import { BNav,BNavItem, BNavText,BNavForm,BNavItemDropdown} from 'bootstrap-vue'
import { BDropdown } from 'bootstrap-vue'
import { BDropdownItem } from 'bootstrap-vue'
import { BToggle } from 'bootstrap-vue'
import { RouterLink, RouterView } from 'vue-router'

Vue.component('router-link', RouterLink)
Vue.component('router-view', RouterView)
Vue.component('b-toggle', BToggle)
Vue.component('b-dropdown', BDropdown)
Vue.component('b-dropdown-item', BDropdownItem)
Vue.component('b-nav', BNav)
Vue.component('b-nav-item', BNavItem)
Vue.component('b-nav-text', BNavText)
Vue.component('b-nav-form', BNavForm)
Vue.component('b-nav-item-dropdown', BNavItemDropdown)

Vue.component('b-navbar', BNavbar)
Vue.component('b-navbar-brand', BNavbarBrand)
Vue.component('b-navbar-toggle', BNavbarToggle)
Vue.component('b-navbar-nav', BNavbarNav)
Vue.component('b-row', BRow)
Vue.component('b-col', BCol)
Vue.component('b-container', BContainer)
Vue.component('b-card', BCard)
Vue.component('b-collapse', BCollapse)
Vue.component('b-button', BButton)
Vue.component('b-spinner', BSpinner)
Vue.component('b-table', BTable)
Vue.component('b-form-checkbox-group', BFormCheckboxGroup)
Vue.component('b-form-checkbox', BFormCheckbox)
Vue.component('b-form-select', BFormSelect)
Vue.component('b-form-input', BFormInput);
Vue.component('b-form-group', BFormGroup);

Vue.component('tuxlog-input', tuxlogInput);
Vue.component('tuxlog-option', tuxlogOption);
Vue.component('tuxlog-checkbox', tuxlogCheckbox);
Vue.component('tuxlog-call-history', tuxlogCallHistory);
Vue.component('tuxlog-call-history-filter', tuxlogCallHistoryFilter);
Vue.component('tuxlog-rigctl', tuxlogRigctl);
Vue.component('tuxlog-menu', tuxlogMenu);

import { VBToggle } from 'bootstrap-vue'
Vue.directive('b-toggle', VBToggle)

import { ToastPlugin } from 'bootstrap-vue'
Vue.use(ToastPlugin)

export const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [
    { path: '/ui', component: {template: '<div>home</div>'} },
    { path: '/ui/about', component: {template: '<div>about</div>'} },
    { path: '/ui/contact', component: {template: '<div>contact</div>'} },
    { path: '/ui/qso', component: Qso },
    { path: '/ui/dataview/:table/:view', component: tuxlogDataView, props:true },
    { path: '/ui/rig/:id', component: Rig, props: true}
    ]
  });


new Vue({
  router,
  template: `
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand :to="{path: '/ui'}">tuXlog</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="#">dk9mbs.de</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">

        <b-nav-item-dropdown text="QSO" right>
        <b-dropdown-item :to="{path: '/ui/qso'}">Add / edit / search a qso</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown text="System" right>
          <b-dropdown-item :to="{path: '/ui/dataview/LogRigs/default'}">Rigs</b-dropdown-item>
          <b-dropdown-item :to="{path: '/ui/dataview/LogLogbooks/default'}">Logbooks</b-dropdown-item>
          <b-dropdown-item :to="{path: '/ui/dataview/LogModes/default'}">Modes</b-dropdown-item>
          <b-dropdown-item :to="{path: '/ui/dataview/LogQslshipmentmodes/default'}">Shipmentmodes</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown text="Help" right>
        <b-dropdown-item :to="{path: '/ui/about'}">About</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown right>
          <template slot="button-content"><em>User</em></template>
          <b-dropdown-item href="#">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
  <router-view class="view" :key="$route.fullPath"></router-view>
  
</div>
`
}).$mount('#app');
