<template>
<div>
    <div v-if="dataform_def_not_found===true" style="background-color: orange;width:100%;">
      No definition found for form: {% raw %}{{ table }} {{ form }}{% endraw %} 
    </div>

    <b-container fluid>
      <b-row class="my-1" key="type" style="background-color: light-grey; padding-bottom:0px">
        <b-col>
            <!--{% raw %}{{ datasource }}{% endraw %}-->
            <tuxlog-rig v-model="datasource[0]"></tuxlog-rig>

        </b-col>  
      </b-row>
    </b-container>
</div>

</template>

<script>
import axios from 'axios'

export default {
  name: 'tuxlog-dataform',
  props: ["id", "table", "form"],
  data() { return {
    dataform_def_not_found: false,
    datasource: {}
}
  },
  mounted () {
    debugger;
    var where=encodeURI("id='"+this.id+"'");
    axios.get('/api/v1.0/tuxlog/'+this.table+'?where='+where).then ( (response) => {
        this.datasource=response.data;
    }).catch((response) => { debugger;this.dataview_def_not_found=true; })

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
    resetErrors() {
      this.dataview_def_not_found=false;
    },
    makeToast(append = false, text) {
      this.toastCount++
      this.$bvToast.toast(text, {
        title: 'tuxlog',
        autoHideDelay: 5000,
        appendToast: append
      })
    },
    handleClick: function(record, index) {
      this.$emit('basedata_list_on_click', record, index);
    },
    handleDblClick: function(record, index) {
      this.$router.push( {path: this.open_path.replace("$1", record.id) } );
      this.$emit('basedata_list_on_dblclick', record, index);
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
