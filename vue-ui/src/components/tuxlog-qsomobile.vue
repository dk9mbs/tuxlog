<template>
<div>

  <div>
    <b-container fluid>
      <b-row class="my-1">
        <!-- 1. Spalte -->
        <b-col style="min-width: 75%; max-width: 100%">
          <b-card class="mb-1">

            <b-container fluid style="font-size:10px;">
              <b-row>
                  <div style="float: left;">
                  <tuxlog-button label="Start" @click="newRecord()" style="min-width:200px;padding-right:5px;"/>
                  <tuxlog-button label="Save" @click="save()" style="min-width:200px;padding-right:5px;"/>
                  <tuxlog-button label="Cancel" @click="cancel()" style="min-width:200px;padding-right:5px;"/>
                   <div style="border-radius:10px;margin-top:5px;min-height: 10px;background-color: red;padding:2px;" v-show="isNewRecordMode()">
                    QSO&nbsp;running&nbsp;...{{ validateForm() }}
                  </div>     
                  </div>

              </b-row>
            </b-container>

          </b-card>  


          <!--<b-card class="mb-1">-->
            <div v-if="appstatus.processdatadetail===true" class="d-flex justify-content-center mb-3">
                <b-spinner label="Loading..."></b-spinner>
            </div>

            <b-container fluid v-if="appstatus.processdatadetail===false">

            <b-row class="mb-1">
              <b-col>
                <tuxlog-option id="lookbook" tooltip="Select the current loogbook. You can manage more the one logbook in one database." v-bind:values="logbooks" v-if="logentry.logbook" v-model="logentry.logbook.id" label="My call"></tuxlog-option>
                <tuxlog-option id="mode" tooltip="Select the current mode" v-bind:values="modes" v-if="logentry.mode" v-model="logentry.mode.id" label="Mode"></tuxlog-option>
                <tuxlog-option id="rig" tooltip="Select the current rig" v-bind:values="rigs" v-if="logentry.rig" v-model="logentry.rig.id" label="Rig"></tuxlog-option>
                <tuxlog-input id="power" type="number" v-model="logentry.power" label="Pwr"></tuxlog-input>
                <tuxlog-input id="frequency" type="number" v-model="logentry.frequency" label="QRG"></tuxlog-input>
                <tuxlog-input id="logdata_utc" readonly=true type="date" v-model="logentry.logdate_utc" label="Date"></tuxlog-input>
                <tuxlog-input id="start_utc" readonly=true type="time" v-model="logentry.start_utc" label="UTC"></tuxlog-input>
                <tuxlog-input id="yourcall" mandatory type="text" @onchange_value="yourcall_onchange" v-model="logentry.yourcall" label="Call"></tuxlog-input>
                <tuxlog-input id="rxrst" tooltip="Your incoming RST, as given by the other station" type="number" v-model="logentry.rxrst" label="RX RST"></tuxlog-input>
                <tuxlog-input id="txrst" tooltip="Your outgoing RST" type="number" v-model="logentry.txrst" label="TX RST"></tuxlog-input>
                <tuxlog-input id="name" type="text" v-model="logentry.name" label="Name"></tuxlog-input>
                <tuxlog-input id="comment" type="text" v-model="logentry.comment" label="Comment"></tuxlog-input>
              </b-col>
            </b-row>
      
            </b-container>
            <!--</b-card>-->


            <tuxlog-rigctl
            v-if="logentry.rig"
            :rig="logentry.rig.id"
            :showpanel="false"
            :showstatus="true"
            @onget_qrg="on_get_qrg">
          </tuxlog-rigctl>
        </b-col>
      </b-row>
</b-container>


  </div>

</div>

</template>

<script>
import { debuglog } from 'util';
import { truncate } from 'fs';
import  {Tuxlog, ifnull}  from '../common.js'

export default {
  name: 'qso1',
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
    }
  },
  mounted () {
    
    var recordId=0;
    var para= new URLSearchParams(window.location.search);
    if(para.has('recordid')) recordId=para.get('recordid');
    this.initEntry(recordId);

    Tuxlog.webRequestAsync('GET','/api/v1.0/tuxlog/LogLogbooks?where='+encodeURI('id <> \'*\''), undefined,(response) => {
      this.logbooks=response.data;
    },(response) => { alert('Error loading lookbooks') })

    Tuxlog.webRequestAsync('GET','/api/v1.0/tuxlog/LogRigs', undefined,(response) => {
      this.rigs=response.data;
    },(response) => { alert('Error loading qslshipmentmodes') })

    Tuxlog.webRequestAsync('GET','/api/v1.0/tuxlog/LogModes', undefined,(response) => {
      this.modes=response.data;
    },(response) => { alert('Error loading qslshipmentmodes') })

    Tuxlog.webRequestAsync('GET','/api/v1.0/tuxlog/LogQslshipmentmodes', undefined,(response) => {
      this.qslshipmentmodes=response.data;
    },(response) => { alert('Error loading qslshipmentmodes') })
    
    
  },
  watch: {
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
      Tuxlog.webRequestAsync('GET','/api/v1.0/callbook/hamdb/'+event,undefined,
      (response)=>{
        this.logentry.name=response.data.haminfo.name
        this.logentry.country=response.data.haminfo.country
        this.logentry.qth=response.data.haminfo.qth
        this.logentry.locator=response.data.haminfo.locator
        this.$forceUpdate();
        },
        (response) => {
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
      } else {
          Tuxlog.webRequestAsync('GET','/api/v1.0/tuxlog/LogLogs/'+id,undefined,
            (response) => {
              this.logentry=response.data;
              console.log(this.logentry);
              this.appstatus.processdatadetail=false;
          },
          (response) => { 
            alert('Fehler'); 
            this.clearForm(); }
          );

      }
    },
    clearForm: function() {
      var now = new Date();
      var utcTime = now.getUTCHours()+":"+now.getUTCMinutes();
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

      var callBackOk=(response) => {
        this.clearForm();
        this.makeToast(true, 'record saved!', 'success');
        this.endQso();
      }

      var callBackErr=(response) => {
        debugger;
        alert('Fehler'); 
        this.appstatus.processdatadetail=false;    
      }

      Tuxlog.webRequestAsync(ifnull(this.logentry.id,'POST', 'PUT') ,
        '/api/v1.0/tuxlog/LogLogs'+ifnull(this.logentry.id,'', '/'+this.logentry.id), 
        this.logentry, callBackOk, callBackErr);

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
