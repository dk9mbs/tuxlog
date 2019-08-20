<template>
<div style="margin-top:0px;">
    <b-form-input placeholder="Call" size="sm" v-model="search.call" @input="handleInput($event, 'call')" ></b-form-input>
    <b-button v-on:click="resetFilter()" size="sm" style="margin-top: 10px;">Reset</b-button>
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
      var pagesize=10;
  
      if (this.search['call'] != null) {
        where=where+"yourcall like '" + this.search['call'] + "%%'";
      }
  
      var paras='order='+encodeURI(orderby)+"&"+'where='+encodeURI(where);
      this.value.listuri=paras;
      this.$emit('input', this.value)
  
      }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
