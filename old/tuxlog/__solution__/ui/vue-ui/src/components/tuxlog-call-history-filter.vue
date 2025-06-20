<template>
<div style="margin-top:0px;">
  <b-form-input style="float: left" placeholder="Call" size="sm" class="mb-1" v-model="search.call" @input="handleInput($event, 'call')" >
  </b-form-input>
  <!--<tuxlog-button label="xd" @click="resetFilter()" style="min-width:200px;float: left;"/>-->
    
    
</div>
</template>

<script>
export default {
  name: 'tuxlog-call-history-filter',
   data() { return{
      "search": {"call": null, "comment": null}
    }},
  props: ["value"],
    methods: {
      handleInput (e, field) {
        this.search[field]=e;
        this.execute();
      },
      resetFilter() {
        this.value.listuri=null;
        this.search.call=null;
      },
      execute() {
      var orderby="logdate_utc desc, start_utc desc";
      var where="";
      var pagesize=50;
  
      if (this.search['call'] != null) {
        where=where+"yourcall like '" + this.search['call'] + "%%'";
      }
  
      var paras='order='+encodeURI(orderby)+"&"+'where='+encodeURI(where)+'&pagesize='+pagesize;
      this.value.listuri=paras;
      this.$emit('input', this.value)
  
      }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
