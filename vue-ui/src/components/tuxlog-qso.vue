<template>
<div>

  <div>
    <b-container fluid>
      <b-row class="my-1" key="type">
        <!-- 1. Spalte -->
        <b-col style="min-width: 75%; max-width: 100%">
          <b-card class="mb-1">

            <b-container fluid style="font-size:10px;">
              <b-row>
                <b-col><tuxlog-button label="Start" @click="newRecord()" style="min-width:200px;"/></b-col>
                <b-col><tuxlog-button label="Save" @click="save()" style="min-width:200px;"/></b-col>
                <b-col><tuxlog-button label="Cancel" @click="cancel()" style="min-width:200px;"/></b-col>
                <b-col>
                  <div style="border-radius:10px;" v-show="isNewRecordMode()">
                    QSO&nbsp;running&nbsp;...{{ validateForm() }}
                  </div>          
                </b-col>
                <b-col>
                    <tuxlog-rigctl
                    v-if="logentry.rig"
                    :rig="logentry.rig.id"
                    :showpanel="false"
                    :showstatus="true"
                    @onget_qrg="on_get_qrg">
                  </tuxlog-rigctl>
                </b-col>
                <b-col>
                  <tuxlog-call-history-filter 
                    v-model="callhistory">
                  </tuxlog-call-history-filter>

                </b-col>
                <b-col></b-col>
              </b-row>
            </b-container>

          </b-card>  


          <b-card class="mb-1">
            <div v-if="appstatus.processdatadetail===true" class="d-flex justify-content-center mb-3">
                <b-spinner label="Loading..."></b-spinner>
            </div>

            <b-container fluid v-if="appstatus.processdatadetail===false">

            <b-row class="mb-1" key="type">
              <b-col>
                <tuxlog-option id="lookbook" tooltip="Select the current loogbook. You can manage more the one logbook in one database." v-bind:values="logbooks" v-if="logentry.logbook" v-model="logentry.logbook.id" label="My call"></tuxlog-option>
              </b-col>
              <b-col>
                <tuxlog-option id="mode" tooltip="Select the current mode" v-bind:values="modes" v-if="logentry.mode" v-model="logentry.mode.id" label="Mode"></tuxlog-option>
              </b-col>
              <b-col>
                <tuxlog-option id="rig" tooltip="Select the current rig" v-bind:values="rigs" v-if="logentry.rig" v-model="logentry.rig.id" label="Rig"></tuxlog-option>
              </b-col>
            </b-row>
      
            <b-row class="mb-1" key="type">
              <b-col>
                <tuxlog-input id="power" type="number" v-model="logentry.power" label="Pwr"></tuxlog-input>
              </b-col>
              <b-col>
                  <tuxlog-input id="frequency" type="number" v-model="logentry.frequency" label="QRG"></tuxlog-input>
              </b-col>
          </b-row>

          <b-row class="mb-1" key="type">
              <b-col>
                <tuxlog-input id="logdata_utc" type="date" v-model="logentry.logdate_utc" label="Date"></tuxlog-input>
            </b-col>
            <b-col>
                <tuxlog-input id="start_utc" type="text" v-model="logentry.start_utc" label="UTC"></tuxlog-input>
            </b-col>
          </b-row>


          <b-row class="mb-1" key="type">
              <b-col>
                  <tuxlog-input id="yourcall" mandatory type="text" @onchange_value="yourcall_onchange" v-model="logentry.yourcall" label="Call"></tuxlog-input>
                </b-col>
              <b-col>
                <tuxlog-input id="rxrst" tooltip="Your incoming RST, as given by the other station" type="number" v-model="logentry.rxrst" label="RX RST"></tuxlog-input>
              </b-col>
            <b-col>
                <tuxlog-input id="txrst" tooltip="Your outgoing RST" type="number" v-model="logentry.txrst" label="TX RST"></tuxlog-input>
              </b-col>
          </b-row>
      
          <b-row class="mb-1" key="type">
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
      
          <b-row class="mb-1" key="type">
            <b-col>
              <tuxlog-input id="name" type="text" v-model="logentry.name" label="Name"></tuxlog-input>
            </b-col>
            <b-col>
              <tuxlog-input id="comment" type="text" v-model="logentry.comment" label="Comment"></tuxlog-input>
            </b-col>
          </b-row>                
      
          <b-row class="mb-1" key="type">
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
                  <tuxlog-input id="dok" tooltip="German DOK" type="text" v-model="logentry.dok" label="DOK"></tuxlog-input>
                </b-col>
            </b-row>
      
      
            <b-row class="mb-1" key="type">
              <b-col>
                <tuxlog-input tooltip="Enter here the via call for qsl routing." id="viacall" type="text" v-model="logentry.viacall" label="via"></tuxlog-input>
              </b-col>
              <b-col>
                <tuxlog-option id="qsl_shipmentmode" v-bind:values="qslshipmentmodes" v-if="logentry.qsl_shipmentmode" v-model="logentry.qsl_shipmentmode.id" label="Shipment"></tuxlog-option>
              </b-col>
          </b-row>
      
      
          <b-row class="mb-1" key="type" >
              <b-col>
                  <tuxlog-checkbox id="qslsend" tooltip="Switch on when you have send your QSL card." v-model="logentry.qslsend" label="Send"></tuxlog-checkbox>
                </b-col>
              <b-col>
                  <tuxlog-checkbox id="qslrecv" tooltip="Switch on if you have recive the QSL card by the other station." v-model="logentry.qslrecv" label="Recv"></tuxlog-checkbox>
                </b-col>
          </b-row>                  
      
            </b-container>
            </b-card>


          <div class="mb-1" style="height: 100px; overflow: auto;font-size:10px;">
          <tuxlog-call-history 
          style="padding-top:5px;"
          v-bind:items="history" 
          v-bind:fields="historyfields" 
          v-bind:id="history" 
          v-bind:pending="appstatus.loadhistory"
          @onclick_row="onclick_history">
          </tuxlog-call-history>
          </div>


        </b-col>

        <!-- 2. Spalte History -->
        <b-col style="max-width:25%"   v-if="1===0">
        </b-col>

      </b-row>
</b-container>


  </div>

</div>

</template>

<script>
import axios from 'axios'
import { debuglog } from 'util';
import { truncate } from 'fs';

export default {
  name: 'qso',
  data() { return {
      appstatus: {"processdatadetail": false, "loadhistory": false, "inqso": false},
      alert: {message: null, type: 'warning',dismissSecs: 10,dismissCountDown: 0,showDismissibleAlert: false},
      logentry: {},
      rigs: [],
      modes: [],
      logbooks: [],
      qslshipmentmodes: [],
      alert: {message: null, type: 'warning',dismissSecs: 10,dismissCountDown: 0,showDismissibleAlert: false}, 
      auth: {username: 'guest', password:null},
      history: [],
      historyfields: ["yourcall","logdate_utc","frequency","mode"],
      callhistory: {"listuri": null, "defaultlisturl": "order=id desc&pagesize=100"}
    }
  },
  mounted () {
    //debugger;
    
    var recordId=0;
    var para= new URLSearchParams(window.location.search);
    if(para.has('recordid')) recordId=para.get('recordid');
    this.initEntry(recordId);

    axios.get('/api/v1.0/tuxlog/LogLogbooks').then( (response) => {
      this.logbooks=response.data;
    }
    ).catch( (response) => { alert('Error loading lookbooks') } )

    axios.get('/api/v1.0/tuxlog/LogRigs').then( (response) => {
      this.rigs=response.data;
    }
    ).catch( (response) => { alert('Error loading rigs') } )

    axios.get('/api/v1.0/tuxlog/LogModes').then( (response) => {
      this.modes=response.data;
    }
    ).catch( (response) => { alert('Error loading modes') } )

    axios.get('/api/v1.0/tuxlog/LogQslshipmentmodes').then( (response) => {
      this.qslshipmentmodes=response.data;
    }
    ).catch( (response) => { alert('Error loading qslshipmentmodes') } )
    
    this.loadHistory();
    
  },
  watch: {
    'callhistory.listuri': function (newValue) {
      //debugger;
      this.appstatus.loadHistory=true;

      if(newValue==null) {
        newValue=this.callhistory.defaultlisturl;
      }

      axios.get('/api/v1.0/tuxlog/LogLogs?'+newValue).then( (response) => {
      this.history=response.data;
      this.appstatus.loadhistory=false;
      }).catch((response)=> {alert('Fehler')})
    }
  },
   filters:{
      getconfigkey: function(value,key){
          if(value==null) return null;
          return value[key];
        }
    },
  methods: {
    on_get_qrg: function(f) {
      if(this.logentry.id==null || this.logentry.id==undefined) {
        this.logentry.frequency=f/1000000;
      }
    },
    onclick_history: function(record, index) {
      this.initEntry(record.id);
    },
    loadHistory: function(callsign="") {
        var paras = "";
        if (this.callhistory.listuri==null) {
          paras=this.callhistory.defaultlisturl;
        } else {
          paras=this.callhistory.listuri;
        }
        
        axios.get('/api/v1.0/tuxlog/LogLogs?'+paras).then( (response) => {
        this.history=response.data;
        this.appstatus.loadhistory=false;
      }).catch((response)=> {alert('Fehler')})
    },
    makeToast(append = false, text, variant='default') {
        this.toastCount++
        this.$bvToast.toast(text, {
          title: 'tuxlog',
          autoHideDelay: 5000,
          appendToast: append,
          variant:variant
        })
      },
    yourcall_onchange: function(event) {
      this.makeToast(true, 'Reading from callbook...')
      this.loadHistory(event);
      axios.get('/api/v1.0/callbook/hamdb/'+event).then((response)=>{
        this.logentry.name=response.data.haminfo.name
        this.logentry.country=response.data.haminfo.country
        this.logentry.qth=response.data.haminfo.qth
        this.logentry.locator=response.data.haminfo.locator
        this.$forceUpdate();
    }).catch((response) => {
      this.logentry.name=""
      this.logentry.country=""
      this.logentry.qth=""
      this.logentry.locator=""
      this.$forceUpdate();
      this.showAlert('Error loading haminfo => '+response, "warning")
    })
    },
    initEntry: function (id) {
      this.appstatus.processdatadetail=true;
      if (id==0) {
        this.clearForm();
      } else {axios.get('/api/v1.0/tuxlog/LogLogs/'+id).then( (response) => {
          this.logentry=response.data;
          console.log(this.logentry);
          this.appstatus.processdatadetail=false;
        }).catch( (response) => { alert('Fehler'); this.clearForm(); } )
      }
    },
    clearForm: function() {
      var now = new Date();
      var utcTime = now.getUTCHours()+":"+now.getUTCMinutes();
      this.loadHistory();
      this.appstatus.processdatadetail=false;

      var rigId="";
      var modeId="";
      var logbookId="";
      var frequency=0;
      var pwr=0
      if (this.logentry.rig!=undefined) rigId=this.logentry.rig.id;
      if (this.logentry.mode!=undefined) modeId=this.logentry.mode.id;
      if (this.logentry.logbook!=undefined) logbookId=this.logentry.logbook.id;
      if (this.logentry.frequency!=undefined) frequency=this.logentry.frequency;
      if (this.logentry.power!=undefined) pwr=this.logentry.power;
      
      this.logentry={"rig": {"id": rigId}, "mode": {"id": modeId}, 
      "logbook": {"id":logbookId}, "qsl_shipmentmode": {"id":"bureau"}, "logdate_utc": new Date().toISOString().slice(0,10), 
      "start_utc": utcTime, "qslsend":0, "qslrecv":0, "frequency": frequency, "power": pwr};

      
    },
    save: function() {
      if(!this.validateForm()) {
        this.makeToast(true,"fill all mandatory fields!", 'danger');
        return;
      }
      axios.post('/api/v1.0/tuxlog/LogLogs', this.logentry).then((response) => {
        //console.log(this.logentry);
        this.clearForm();
        this.makeToast(true, 'record saved!', 'success');
        this.endQso();
      }).catch((response)=>{alert('Fehler'); this.appstatus.processdatadetail=false; })
    },
    countDownChanged: function(dismissCountDown) {
      this.alert.dismissCountDown = dismissCountDown
    },
    showAlert: function(message, type='warning') {
      this.alert.message=message;
      this.alert.type=type;
      this.alert.dismissCountDown = this.alert.dismissSecs;
    },
    endQso() {
      this.appstatus.inqso=false;
    },
    cancel() {
        this.clearForm();
        this.endQso();
    },
    newRecord() {
      if(this.isNewRecordMode()==true) {
        this.makeToast(true,"Please save or cancel first!", 'warning');
        return;
      }
      this.appstatus.inqso=true;
      this.clearForm();
    },
    isNewRecordMode() {
      return this.appstatus.inqso && this.logentry.id==undefined ;
    },
    isInEditMode(){
      return ! (this.logentry.id==null || this.logentry.id==undefined || this.logentry.id==0)
    },
    validateForm() {
      if (this.logentry.yourcall==undefined || this.logentry.yourcall=="") return false;
      if (this.logentry.rxrst==undefined || this.logentry.rxrst=="") return false;
      if (this.logentry.txrst==undefined || this.logentry.txrst=="") return false;
      if (this.logentry.rig==undefined) return false;
      if (this.logentry.mode==undefined) return false;
      if (this.logentry.logbook==undefined) return false;
      if (this.logentry.frequency==undefined || this.logentry.frequency==0) return false;

      return true;
    }

  }
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
