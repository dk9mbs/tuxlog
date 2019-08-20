//import Vue from 'vue'
import Vue from 'vue/dist/vue.esm.js'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.config.productionTip = false
/*
new Vue({
  render: h => h(App),
}).$mount('#app')
*/

var vue=new Vue({
  el: '#app',
  data () {
    return {
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
      callhistory: {"listuri": null, "defaultlisturl": "order=id desc&pagesize=10"}
    }
  },
  mounted () {
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
})
