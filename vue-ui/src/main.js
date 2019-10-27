import Vue from 'vue'
import { Tuxlog } from './common.js'

import Qso from './components/tuxlog-qso.vue'
import Rig from './components/tuxlog-rig.vue'

import VueRouter from 'vue-router';
Vue.use(VueRouter);

import axios from 'axios'
import tuxlogInput from './components/tuxlog-input.vue'
import tuxlogOption from './components/tuxlog-option.vue'
import tuxlogCheckbox from './components/tuxlog-checkbox.vue'
import tuxlogButton from './components/tuxlog-button.vue'
import tuxlogCallHistory from './components/tuxlog-call-history.vue'
import tuxlogCallHistoryFilter from './components/tuxlog-call-history-filter.vue'
import tuxlogRigctl from './components/tuxlog-rigctl.vue'
import tuxlogDataView from './components/tuxlog-dataview.vue'
import tuxlogDataForm from './components/tuxlog-dataform.vue';
import tuxlogRig from './components/tuxlog-rig.vue';
import tuxlogQslshipmentmode from './components/tuxlog-qslshipmentmode';
import tuxlogMode from './components/tuxlog-mode';
import tuxlogLogbook from './components/tuxlog-logbook';


import { BFormInput, BInputGroupText } from 'bootstrap-vue'
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
import { BInputGroup } from 'bootstrap-vue'
import { PopoverPlugin } from 'bootstrap-vue'
import {PInputGroupText} from 'bootstrap-vue';
import {BModal} from 'bootstrap-vue';

Vue.use(PopoverPlugin)
Vue.component('b-modal', BModal);
Vue.component('b-input-group', BInputGroup);
Vue.component('b-input-group-text', BInputGroupText);
Vue.component('router-link', RouterLink);
Vue.component('router-view', RouterView);
Vue.component('b-toggle', BToggle);
Vue.component('b-dropdown', BDropdown);
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
Vue.component('tuxlog-button', tuxlogButton);
Vue.component('tuxlog-dataform', tuxlogDataForm);
Vue.component('tuxlog-rig', tuxlogRig)
Vue.component('tuxlog-mode', tuxlogMode)
Vue.component('tuxlog-logbook', tuxlogLogbook)
Vue.component('tuxlog-qslshipmentmode', tuxlogQslshipmentmode)


import { VBToggle } from 'bootstrap-vue'
Vue.directive('b-toggle', VBToggle)

import { VBPopover } from 'bootstrap-vue'
Vue.directive('b-popover', VBPopover)

import { ToastPlugin } from 'bootstrap-vue'
Vue.use(ToastPlugin)

import { ModalPlugin } from 'bootstrap-vue'
Vue.use(ModalPlugin)

import LiquorTree from 'liquor-tree';
Vue.use(LiquorTree);

import QsoMobile from './components/tuxlog-qsomobile.vue'
Vue.component('tuxlog-qsomobile', QsoMobile);

import Qsl from './pages/tuxlog-qsl.vue';
Vue.component('tuxlog-qsl', Qsl);

//Tuxlog.setdeviceType('desktop');

export const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [
    { path: '/ui', component: {template: '<div style="padding: 5px;">tuxLog</div>'} },
    { path: '/ui/about', component: {template: '<div>about</div>'} },
    { path: '/ui/contact', component: {template: '<div>contact</div>'} },
    { path: '/ui/qso', component: Qso, meta: {mobile: 'mobile'} },
    { path: '/ui/qso/phone', component: QsoMobile },
    { path: '/ui/dataview/:table/:view', component: tuxlogDataView, props:true },
    { path: '/ui/dataform/:table/:form/:id', component: tuxlogDataForm, props:true },
    { path: '/ui/dataform/:table/:form/', component: tuxlogDataForm, props:true },
    { path: '/ui/qsl', component: Qsl, props:false },
    ]
  });

  router.beforeEach((to, from, next) => {
    if(to.meta.mobile && Tuxlog.isPhone()) {
      next(to.path+'/phone');
    } else {
      next();
    }
  })

new Vue({
  comments: {QsoMobile},
  router,
  data() { return {
    showSidePanel: false
    }
  },
  methods: {
    togleSidePanel: function() {
      this.showSidePanel=!this.showSidePanel;
    },
    onClickMenuItem(node) {
      this.$router.push(node.id);
    },
    setDeviceType: function(e) {
      debugger;
      if(e==0) {
        Tuxlog.setdeviceType('desktop');
      } else {
        Tuxlog.setdeviceType('phone');
      }
    }
  },
  template: `
  <div>
    
    <b-navbar v-if="1===1" toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand :to="{path: '/ui'}">tuxLog</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="#">dk9mbs.de</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">

        <b-nav-item-dropdown text="Qso" right>
          <b-dropdown-item :to="{path: '/ui/qso'}">QSO (desktop)</b-dropdown-item>
          <b-dropdown-item :to="{path: '/ui/qso/phone'}">QSO (phone)</b-dropdown-item>
          <b-dropdown-item :to="{path: '/ui/qsl'}">Qsl management</b-dropdown-item>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown text="System" right>
          <b-dropdown-item :to="{path: '/ui/dataview/LogRigs/default'}">Rigs</b-dropdown-item>
          <b-dropdown-item :to="{path: '/ui/dataview/LogModes/default'}">Modes</b-dropdown-item>
          <b-dropdown-item :to="{path: '/ui/dataview/LogLogbooks/default'}">Logbooks</b-dropdown-item>
          <b-dropdown-item :to="{path: '/ui/dataview/LogQslshipmentmodes/default'}">Qsl shipment</b-dropdown-item>
          <b-dropdown-item :to="{path: '/ui/dataview/LogDxcc/default'}">DXCC entities</b-dropdown-item>
          <b-dropdown-item :to="{path: '/ui/dataview/LogImportjobs/default'}">Importjobs</b-dropdown-item>
          <b-dropdown-item :to="{path: '/ui/dataview/LogBands/default'}">Bänder</b-dropdown-item>
          <b-nav-form>
            <tuxlog-checkbox style="padding-left:20px;" label="Phone" @onchange_value="setDeviceType" />
          </b-nav-form>
        </b-nav-item-dropdown>

        <b-nav-item-dropdown text="Help" right>
          <b-dropdown-item :to="{path: '/ui/about'}">About</b-dropdown-item>
        </b-nav-item-dropdown>

        <!--Tuxlog.setdeviceType('mobile'); -->


        <b-nav-item-dropdown right>
          <template slot="button-content"><em>User</em></template>
          <b-dropdown-item href="#">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>

      </b-navbar-nav>
    </b-collapse>
  </b-navbar>

  <div><router-view class="view" :key="$route.fullPath"/></div>
</div>
`
}).$mount('#app');
