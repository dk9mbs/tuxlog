<template>
  <div>
    <b-card>

      <tuxlog-input label="Call" @input="handleSearch" />

      <b-table :fields="fields" :items="items" :busy="isBusy" :stacked="isStacked"
          striped hover small
          v-bind:bordered="true">
        <template slot="qslrecv" slot-scope="row">
          <span><tuxlog-checkbox v-model="row.item.qslrecv" hidelabel />
          </span>
        </template>
        <template slot="qslsend" slot-scope="row">
          <span><tuxlog-checkbox v-model="row.item.qslsend" hidelabel />
          </span>
        </template>

        <template slot="txrst" slot-scope="row">
          <span><tuxlog-input v-model="row.item.txrst" hidelabel />
          </span>
        </template>

        <template slot="rxrst" slot-scope="row">
          <span><tuxlog-input v-model="row.item.rxrst" hidelabel />
          </span>
        </template>

        <template slot="save" slot-scope="row">
          <span><tuxlog-button label="Save" @onclick="handleSave(row)" />
          </span>
        </template>
      </b-table>
    </b-card>
  </div>
</template>

<script>
//import axios from 'axios'
import { debuglog } from 'util';
import { truncate } from 'fs';
import  {Tuxlog, ifnull}  from '../common.js'

export default {
  name: 'qsl',
  data() { return {
      isBusy: false,
      items: [],
      fields: ["logbook","yourcall","logdate_utc","start_utc","frequency","mode","txrst","rxrst","qslrecv", "qslsend","save"],
    }
  },
  mounted () {
    
    Tuxlog.webRequestAsync('GET','/api/v1.0/tuxlog/LogLogs?where='+encodeURI('id < 0'), undefined,(response) => {
      this.items=response.data;
    },(response) => { alert('Error loading lookbooks') })
    
  },
  watch: {
  },
  filters:{
  },
  computed: {
    isStacked: {
      get: function(){return Tuxlog.isMobil()}
    }
  },
  methods: {
    handleSearch(e) {
      if( String(e).length < 2 ) return;

      Tuxlog.webRequestAsync('GET','/api/v1.0/tuxlog/LogLogs?where='+encodeURI('yourcall like \''+e+'%%\'')+'&pagesize=100', 
        undefined,(response) => {
        this.items=response.data;
      },(response) => { alert('Error loading lookbooks') })
    },
    handleSave(row) {
      console.log(row);
      if(this.isBusy==true) return;

      var callBackOk=(response) => {
        this.makeToast(true, 'record saved!', 'success');
      }

      var callBackErr=(response) => {
        debugger;
        alert('Fehler'); 
      }

      Tuxlog.webRequestAsync('PUT',
        '/api/v1.0/tuxlog/LogLogs', 
        row.item, callBackOk, callBackErr);
    },
        makeToast(append = false, text, variant='default') {
        this.toastCount++
        this.$bvToast.toast(text, {
          title: 'tuxlog',
          autoHideDelay: 500,
          appendToast: append,
          variant:variant
        })
    },

  }
}

</script>