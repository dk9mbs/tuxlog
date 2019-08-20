<template>
<div class="parent" id="app">
  
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#">tuxlog</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="#">dk9mbs.de</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">

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


  <div>
  </div>

  <!--
  <b-tabs style="float:right;">
      <b-tab title="Logentry" active>
-->


  <div>
    <b-container fluid>
      <b-row class="my-1" key="type">
        <b-col>
          
          <b-button variant="outline-secondary" v-b-toggle.collapse-rigctl size="sm" style="margin-top:10px;margin-bottom:5px;">Rig control</b-button>
          <b-collapse id="collapse-rigctl" visible="true" class="mt-2">
            <b-card>
            <tuxlog-rigctl
              rig="ic735">
            </tuxlog-rigctl>
            </b-card>
          </b-collapse>

          <div>
          <tuxlog-call-history 
          style="padding-top:5px;"
          v-bind:items="history" 
          v-bind:fields="historyfields" 
          v-bind:id="history" 
          v-bind:pending="appstatus.loadhistory"
          @onclick_row="onclick_history">
          </tuxlog-call-history>
        </div>

          <b-button variant="outline-secondary" v-b-toggle.collapse-1 size="sm" stye="margin-bottom: 5px;">Call history filter</b-button>
          <b-collapse id="collapse-1" class="mt-2">
              <b-card>
              <tuxlog-call-history-filter 
                v-model="callhistory"
              >
              </tuxlog-call-history-filter>
            </b-card>
          </b-collapse>
        </b-col>

  
        <b-col>
          <b-card>
            <div v-if="appstatus.processdatadetail===true" class="d-flex justify-content-center mb-3">
                <b-spinner label="Loading..."></b-spinner>
            </div>
            <b-container fluid v-if="appstatus.processdatadetail===false">
            <b-row class="my-1" key="type">
              <b-col>
                <tuxlog-option id="lookbook" v-bind:values="logbooks" v-if="logentry.logbook" v-model="logentry.logbook.id" label="My call"></tuxlog-option>
              </b-col>
              <b-col>
                <tuxlog-option id="mode" v-bind:values="modes" v-if="logentry.mode" v-model="logentry.mode.id" label="Mode"></tuxlog-option>
              </b-col>
              <b-col>
                <tuxlog-option id="rig" v-bind:values="rigs" v-if="logentry.rig" v-model="logentry.rig.id" label="Rig"></tuxlog-option>
              </b-col>
            </b-row>
      
            <b-row class="my-1" key="type">
              <b-col>
                <tuxlog-input id="power" type="number" v-model="logentry.power" label="Pwr"></tuxlog-input>
              </b-col>
              <b-col>
                  <tuxlog-input id="frequency" type="number" v-model="logentry.frequency" label="QRG"></tuxlog-input>
                </b-col>
              <b-col>
                <tuxlog-input id="logdata_utc" type="date" v-model="logentry.logdate_utc" label="Date"></tuxlog-input>
            </b-col>
            <b-col>
                <tuxlog-input id="start_utc" type="text" v-model="logentry.start_utc" label="UTC"></tuxlog-input>
            </b-col>
          </b-row>
      
          <b-row class="my-1" key="type">
              <b-col>
                  <tuxlog-input id="yourcall" type="text" @onchange_value="yourcall_onchange" v-model="logentry.yourcall" label="Call"></tuxlog-input>
                </b-col>
              <b-col>
                <tuxlog-input id="rxrst" type="number" v-model="logentry.rxrst" label="RX RST"></tuxlog-input>
              </b-col>
            <b-col>
                <tuxlog-input id="txrst" type="number" v-model="logentry.txrst" label="TX RST"></tuxlog-input>
              </b-col>
          </b-row>
      
          <b-row class="my-1" key="type">
              <b-col>
                  <tuxlog-input id="locator" type="text" v-model="logentry.locator" label="LOC"></tuxlog-input>
              </b-col>
              <b-col>
                <tuxlog-input id="qth" type="text" v-model="logentry.qth" label="QTH"></tuxlog-input>
            </b-col>
            <b-col>
                  <tuxlog-input id="country" type="text" v-model="logentry.country" label="Country"></tuxlog-input>
            </b-col>
          </b-row>
      
          <b-row class="my-1" key="type">
            <b-col>
              <tuxlog-input id="name" type="text" v-model="logentry.name" label="Name"></tuxlog-input>
            </b-col>
            <b-col>
              <tuxlog-input id="comment" type="text" v-model="logentry.comment" label="Comment"></tuxlog-input>
            </b-col>
          </b-row>                
      
          <b-row class="my-1" key="type">
              <b-col>
                  <tuxlog-input id="itu_prefix" type="text" v-model="logentry.itu_prefix" label="Prefix"></tuxlog-input>
                </b-col>
              <b-col>
                  <tuxlog-input id="dxcc" type="text" v-model="logentry.dxcc" label="DXCC"></tuxlog-input>
                </b-col>
              <b-col>
                  <tuxlog-input id="cq" type="text" v-model="logentry.cq" label="CQ"></tuxlog-input>
                </b-col>
              <b-col>
                  <tuxlog-input id="itu" type="text" v-model="logentry.itu" label="ITU"></tuxlog-input>
                </b-col>
              <b-col>
                  <tuxlog-input id="dok" type="text" v-model="logentry.dok" label="DOK"></tuxlog-input>
                </b-col>
            </b-row>
      
      
            <b-row class="my-1" key="type">
              <b-col>
                <tuxlog-input id="viacall" type="text" v-model="logentry.viacall" label="via"></tuxlog-input>
              </b-col>
              <b-col>
                <tuxlog-option id="qsl_shipmentmode" v-bind:values="qslshipmentmodes" v-if="logentry.qsl_shipmentmode" v-model="logentry.qsl_shipmentmode.id" label="Shipment"></tuxlog-option>
              </b-col>
          </b-row>
      
      
          <b-row class="my-1" key="type" style="width: 50%;">
              <b-col>
                  <tuxlog-checkbox id="qslsend" v-model="logentry.qslsend" label="Send"></tuxlog-checkbox>
                </b-col>
              <b-col>
                  <tuxlog-checkbox id="qslrecv" v-model="logentry.qslrecv" label="Recv"></tuxlog-checkbox>
                </b-col>
          </b-row>                  
      
          <b-row class="my-1" key="type" style="width: 50%;">
            <b-col>
              <b-button v-on:click="clearForm()" size="sm">New</b-button>
              <b-button v-on:click="save()" size="sm" v-if="this.appstatus.processdatadetail===false">Save and new</b-button>
      
              </b-col>
            </b-row>        
          </b-container></b-card>

  </b-col>
</b-row>
</b-container>


  </div>
</div>

</template>

<script>
//import Vue from 'vue'
import Vue from 'vue/dist/vue.esm.js'
import tuxlogInput from './components/tuxlog-input.vue'
import tuxlogOption from './components/tuxlog-option.vue'
import tuxlogCheckbox from './components/tuxlog-checkbox.vue'
import tuxlogCallHistory from './components/tuxlog-call-history.vue'
import tuxlogCallHistoryFilter from './components/tuxlog-call-history-filter.vue'
import tuxlogRigctl from './components/tuxlog-rigctl.vue'

import { BFormInput } from 'bootstrap-vue'
import { BFormGroup } from 'bootstrap-vue'
import { BFormSelect } from 'bootstrap-vue'
import { BFormCheckboxGroup } from 'bootstrap-vue'
import { BFormCheckbox } from 'bootstrap-vue'
import { BTable } from 'bootstrap-vue'
import { BSpinner } from 'bootstrap-vue'

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
Vue.component('tuxlog-call-history', tuxlogCallHistoryFilter);
Vue.component('tuxlog-rigctl', tuxlogRigctl);


export default {
  name: 'app'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
