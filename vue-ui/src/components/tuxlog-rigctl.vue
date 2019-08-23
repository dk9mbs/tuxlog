<template>
<div>
      <tuxlog-input id="qrg" type="number" v-model="freq" label="QRG" v-bind:readonly="true"></tuxlog-input>
      <div style="background-color:lightgrey;padding-top: 11px; padding-bottom:10px;padding-left:5px;">
      <b-button pill variant="success" style="margin-bottom: 0px" v-on:click="startInterval()" v-bind:disabled="timer_id != 0" size="sm">></b-button>
      <b-button pill variant="danger" style="margin-bottom: 0px" v-on:click="stopInterval()" v-bind:disabled="timer_id === 0" size="sm">||</b-button>
      <span style="background-color: red; text-align: left; padding:10px;" v-if="error != null">{% raw %}{{ error_text }}{%endraw %}</span>
      <span style="background-color: LightGreen ; text-align: left; padding:10px;" v-if="error === null">{% raw %}{{ rig }}{%endraw %} successfully connected</span>
      <span style="background-color: DarkOrange; text-align: left; padding:10px;" v-if="timer_id === 0">{% raw %}{{ rig }}{%endraw %} connection stopped</span>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
import VueAxios from 'vue-axios'

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
    props: ["qrg", "mode", "rig"],
     mounted() {
    this.startInterval();
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
            axios.get('/api/v1.0/rigctl/'+this.rig+'/f').then(response => {
              this.freq=response.data['response']['Frequency']
              this.error=null
            }).catch( response => {
              console.log(response.response.data['error']);
              this.error= response.response.data;
              this.error_text= response.response.data['error'];
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
