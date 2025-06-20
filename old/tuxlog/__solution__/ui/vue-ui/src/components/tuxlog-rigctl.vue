<template>
<div>

      <div
        v-if="showpanel===true"
        style="border-radius: 10px;padding-top: 11px; padding-bottom:10px;padding-left:5px;margin-top: 3px;">
      <tuxlog-input id="qrg" type="number" v-model="freq" label="QRG" v-bind:readonly="true"></tuxlog-input>
      <b-button pill variant="success" style="margin-bottom: 0px" v-on:click="startInterval()" v-bind:disabled="timer_id != 0" size="sm">></b-button>
      <b-button pill variant="danger" style="margin-bottom: 0px" v-on:click="stopInterval()" v-bind:disabled="timer_id === 0" size="sm">||</b-button>
      <span style="border-radius:10px;font-size:10px;background-color: red; text-align: left; padding:10px;margin-left:3px;" v-if="error != null">{{ error_text }}</span>
      <span style="border-radius:10px;font-size:10px ; text-align: left; padding:10px;margin-left:3px;" v-if="error === null && timer_id!=0">{{ rig }} successfully connected</span>
      <span style="border-radius:10px;font-size:10px;background-color: DarkOrange; text-align: left; padding:10px;margin-left:3px;" v-if="timer_id === 0">{{ rig }} connection stopped</span>
      </div>


      <div
        v-if="showstatus===true"
        style="border-radius: 10px;padding-top: 11px; padding-bottom:10px;padding-left:5px;margin-top: 3px;">
      <span style="min-width: 25px;border-radius:10px;font-size:10px;background-color: red; text-align: left; padding:10px;margin-left:3px;" v-if="error != null"></span>
      <span style="min-width: 25px;border-radius:10px;font-size:10px;background-color: green; text-align: left; padding:10px;margin-left:3px;" v-if="error === null && timer_id!=0"></span>
      <span style="min-width: 25px;border-radius:10px;font-size:10px;background-color: DarkOrange; text-align: left; padding:10px;margin-left:3px;" v-if="timer_id === 0"></span>
      </div>

  </div>
</template>

<script>
import axios from 'axios'
import VueAxios from 'vue-axios'
import  {Tuxlog, ifnull}  from '../common.js'

export default {
  name: 'tuxlog-rigctl',
 data() {
        return {
          freq: 0,
          error: null,
          error_text: "",
          timer_id: 0,
          timer_interval: 1000
      }
    },
    props: {qrg: {}, mode:{}, rig:{}, showpanel:{default: true}, showstatus:{default: false}},
    mounted() {
    this.startInterval();
  },
  destroyed() {
    this.stopInterval();
  },
  watch: {
    rig: function(newRig) {
      this.stopInterval();
      this.startInterval();
    }
  },
  methods: {
      handleInput (event, field) {
        this.$emit('ongetrigdata', field, event)
      },
      stopInterval: function () {
        clearInterval(this.timer_id);
        this.timer_id=0;
      },
      startInterval: function() {
        // use arrow function
        var intervalId=setInterval(() => {
          this.clearError();

          Tuxlog.webRequestAsync('POST','/api/v1.0/webfunction/get_rig_data', {"rig_id": this.rig, "command":"f"} ,
          (response) => {
            debugger;
            this.freq=response.data['response']['Frequency']
            this.error=null
            this.$emit('onget_qrg', this.freq);
          }, (response) => {
            console.log(response['orgres'].response.data['error']);
            this.error= response['orgres'].response.data;
            this.error_text= response['orgres'].response.data['error'];
            this.freq=0;
            this.stopInterval();

          })

      },this.timer_interval )
      this.timer_id=intervalId;
      return intervalId;
    },
    clearError: function() {
      this.error=null;
      this.error_text="";
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
