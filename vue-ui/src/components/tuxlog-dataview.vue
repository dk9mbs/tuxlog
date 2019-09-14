<template>
<div>
    <div v-if="dataview_def_not_found===true" style="background-color: orange;width:100%;">
      No definition found for View: {{ table }} {{ view }} 
    </div>

    <b-container fluid>
      <b-row class="my-1" style="background-color: light-grey; padding-bottom:0px">
        <b-col>
          <b-button pill variant="outline-secondary" @click="handleNewClick"  size="sm" style="margin-top:0px;margin-bottom:0px;">+ new</b-button>
          <b-button pill v-if="selected_id!==undefinied" variant="outline-secondary" @click="handleDelClick"  size="sm" style="margin-top:0px;margin-bottom:0px;">Trash</b-button>
        </b-col>  

        <b-col>
          <tuxlog-input label="Search" style="margin:0px;"></tuxlog-input>
        </b-col>  

      </b-row>
      <b-row class="my-1" >
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
import axios from 'axios';
import encodeIdToURI from '../common.js';

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
      callhistory: {"listuri": null, "defaultlisturl": "order=id desc&pagesize=100"},
      selected_id: undefined
    }
  },
  mounted () {


    var where=encodeURI("model_name='"+this.table+"' AND view_name='"+this.view+"'");
    axios.get('/api/v1.0/tuxlog/MetaDataviews?where='+where).then ( (response) => {
      this.resetErrors();
      this.fields=JSON.parse(response.data[0].fields);
      this.id_field_name=response.data[0].id_field_name;
      this.open_path=response.data[0].open_path;
      this.filter_filter_clause=response.data[0].filter_clause;
      this.order_by=response.data[0].order_by;

      this.loadData();

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
    loadData() {
      var url='/api/v1.0/tuxlog/'+this.table;
      if(this.order_by!=undefined) {
        url=url+'?order='+encodeURI(this.order_by)
      }

      axios.get(url).then( (response) => {
        this.datalist=response.data;
      }
      ).catch( (response) => { alert('Error loading data') } )

    },
    handleNewClick() {
      this.$router.push('/ui/dataform/LogRigs/default/');
    },
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
      this.selected_id=record.id;
      this.$emit('basedata_list_on_click', record, index);
    },
    handleDblClick: function(record, index) {

      this.$router.push( {path: this.open_path.replace("$1",  record.id.replace('/','%2F')   ) } );
      this.$emit('basedata_list_on_dblclick', record, index);
    },
    handleDelClick: function () {

          this.$bvModal.msgBoxConfirm('Are you sure?')
          .then(value => {
            if(value==true){
              axios.delete('/api/v1.0/tuxlog/'+this.table+'/'+this.selected_id.replace('/','%2F'))
                .then((response) => {this.loadData();})
                .catch((error)=> {alert(error); console.log(error)});
              

            }
          })
          .catch(err => {
            // An error occurred
          })


    }



  }
}
</script>

<style>

</style>
