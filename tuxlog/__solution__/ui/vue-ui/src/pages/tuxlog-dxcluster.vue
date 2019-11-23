<template>
  <div>
        <div class="mb-1" style="height: 60vh; overflow: auto;font-size:10px;">
            <b-table :fields="fields" :items="items" :busy="isBusy"
                hover small
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
        </div>
  </div>
</template>

<script>
//import axios from 'axios'
import { debuglog } from 'util';
import { truncate } from 'fs';
import  {Tuxlog, ifnull}  from '../common.js'
import axios from 'axios';

export default {
  name: 'qsl',
  data() { return {
      isBusy: false,
      items: [],
      fields: ["spotter","dxcc","country","continent","frequency","band","dx","dx_dxcc","dx_country","dx_continent", "comment","time_utc"],
    }
  },
  mounted () {
      this.getClusterData();
  },
  watch: {
  },
  filters:{
  },
  computed: {
  },
  methods: {
      'getClusterData':  function () {
            Tuxlog.webRequestAsync('GET','/api/v1.0/tuxlog/LogVwDxclusterSpots?pagesize=50', undefined,(response) => {
                this.items=response.data;
                window.setTimeout(this.getClusterData, 5000);
            },(response) => { 
                alert('Error loading cluster data. Pse restart!') ;
            })
      } //fn
  }
}

</script>