<template>
<div>
    <div v-if="dataview_def_not_found===true" style="background-color: orange;width:100%;">
      No definition found for View: {% raw %}{{ table }} {{ view }}{% endraw %} 
    </div>

    <b-container fluid>
      <b-row class="my-1" key="type">
        <b-col>
          <div style="height:500px; overflow: auto;">
            <b-table
              striped hover small
              v-bind:bordered="true" v-bind:items="datalist" v-bind:fields="fields" 
                @row-clicked="handleClick"
                @row-dblclicked="handleDblClick"
              >
            </b-table>
          </div>
        </b-col>
      </b-row>
    </b-container>
</div>

</template>

<script>
import axios from 'axios'

export default {
  name: 'tuxlog-dataview',
  props: ["data", "table", "view"],
  data() { return {
      dataview_def_not_found: false,
      datalist: [],
      fields: ["id"],
      id_field_name: "id",
      open_path: "",
      order_by: "",
      callhistory: {"listuri": null, "defaultlisturl": "order=id desc&pagesize=100"}
    }
  },
  mounted () {


    var where=encodeURI("table_name='"+this.table+"' AND view_name='"+this.view+"'");
    axios.get('/api/v1.0/tuxlog/MetaDataviews?where='+where).then ( (response) => {
      debugger;
      this.resetErrors();
      this.fields=JSON.parse(response.data[0].fields);
      this.id_field_name=response.data[0].id_field_name;
      this.open_path=response.data[0].open_path;
      this.filter_filter_clause=response.data[0].filter_clause;
      this.order_by=response.data[0].order_by;

      var url='/api/v1.0/tuxlog/'+this.table;
      if(this.order_by!=undefined) {
        url=url+'?order='+encodeURI(this.order_by)
      }

      axios.get(url).then( (response) => {
        this.datalist=response.data;
      }
      ).catch( (response) => { alert('Error loading lookbooks') } )


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
      //this.$router.push( {path: 'ui/rig/'+record.id } );
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
