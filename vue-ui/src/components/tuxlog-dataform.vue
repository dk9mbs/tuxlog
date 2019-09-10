<template>
<div>
    <div v-if="dataform_def_not_found===true" style="background-color: orange;width:100%;">
      No definition found for form: {% raw %}{{ table }} {{ form }}{% endraw %} 
    </div>

    <b-card class="mb-1 ml-1 mr-1 mt-1">
      <b-container fluid>
        <b-row class="my-1" key="type" style="background-color: light-grey; padding-bottom:0px">
          <b-col>

              <component :is="datacomponent" v-model="currentrecord"></component>

          </b-col>  
        </b-row>

      </b-container>
    </b-card>

    <b-card class="mb-1 ml-1 mr-1 mt-1">
      <tuxlog-button @click="save" label="Save"/>
    </b-card>
</div>

</template>

<script>
import axios from 'axios'

export default {
  name: 'tuxlog-dataform',
  props: ["id", "table", "form"],
  data() { return {
    dataform_def_not_found: false,
    datasource: [],
    currentrecord: {},
    datacomponent: ""
}
  },
  mounted () {
    var where=encodeURI("id='"+this.id+"'");
    axios.get('/api/v1.0/tuxlog/'+this.table+'?where='+where).then ( (response) => {
        this.datasource=response.data;
        this.currentrecord=this.datasource[0];
    }).catch((response) => { debugger;alert('Error in dataform'+where); })

    var where=encodeURI("model_name='"+this.table+"' AND form_name='"+this.form+"'");
    axios.get('/api/v1.0/tuxlog/MetaDataforms?where='+where).then((response) => {
      this.datacomponent=response.data[0].datacomponent;
    }).catch((response) => {
      this.dataview_def_not_found=true; 
    });

  },
  watch: {
  },
  filters:{
  },
  methods: {
    makeToast(append = false, text) {
      this.toastCount++
      this.$bvToast.toast(text, {
        title: 'tuxlog',
        autoHideDelay: 5000,
        appendToast: append
      })
    },
    save: function() {
      axios.post('/api/v1.0/tuxlog/'+this.table, this.currentrecord).then((response) => {
        //this.clearForm();
        //this.makeToast(true, 'record saved!', 'success');
        //this.endQso();
        alert('Gespeichert');
      }).catch((response)=>{alert('Fehler'); this.appstatus.processdatadetail=false; })
    },
  }
}
</script>

<style>
</style>
