<template>
<div>
  <div>
    <b-container fluid>
      <b-row class="my-1" key="type">
        <b-col>
          
          <b-button variant="outline-secondary" v-b-toggle.collapse-rigctl size="sm" style="margin-top:10px;margin-bottom:5px;">Rig control</b-button>
          <b-collapse id="collapse-rigctl" v-bind:visible="true" class="mt-2">
            <b-card>
            <tuxlog-rigctl
              rig="ic735">
            </tuxlog-rigctl>
            </b-card>
          </b-collapse>

          <div style="height: 400px; overflow: auto;">
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
import axios from 'axios'

export default {
  name: 'qso',
  data() { return {
      appstatus: {"processdatadetail": false, "loadhistory": false},
      alert: {message: null, type: 'warning',dismissSecs: 10,dismissCountDown: 0,showDismissibleAlert: false},
      logentry: {},
      rigs: [],
      modes: [],
      logbooks: [],
      qslshipmentmodes: [],
      alert: {message: null, type: 'warning',dismissSecs: 10,dismissCountDown: 0,showDismissibleAlert: false}, 
      auth: {username: 'guest', password:null},
      history: [],
      historyfields: ["id", "yourcall", "start_utc","logdate_utc","frequency","rxrst"],
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
    onclick_history: function(record, index) {
      console.log('selected record => '+record);
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
     makeToast(append = false, text) {
        this.toastCount++
        this.$bvToast.toast(text, {
          title: 'tuxlog',
          autoHideDelay: 5000,
          appendToast: append
        })
      },
    yourcall_onchange: function(event) {
      debugger;
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
      
      this.logentry={"rig": {"id": "ic735"}, "mode": {"id": "SSTV"}, 
      "logbook": {"id":"dk9mbs"}, "qsl_shipmentmode": {"id":"bureau"}, "logdate_utc": new Date().toISOString().slice(0,10), 
      "start_utc": utcTime, "qslsend":0, "qslrecv":0};
    },
    save: function() {
      axios.post('/api/v1.0/tuxlog/LogLogs', this.logentry).then((response) => {
        console.log(this.logentry);
        this.clearForm();
        this.makeToast(true, 'New entry saved!');
      }).catch((response)=>{alert('Fehler'); this.appstatus.processdatadetail=false; })
    },
    countDownChanged: function(dismissCountDown) {
      this.alert.dismissCountDown = dismissCountDown
    },
    showAlert: function(message, type='warning') {
      this.alert.message=message;
      this.alert.type=type;
      this.alert.dismissCountDown = this.alert.dismissSecs;
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
