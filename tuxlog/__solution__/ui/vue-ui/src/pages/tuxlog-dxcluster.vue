<template>
  <div>
        <div class="mb-1" style="overflow: auto;font-size:10px;background-color:inherit;">
        <tuxlog-checkbox v-for="(item, index) in bands" v-model="bands[index]['show_dxspots']" 
            :key="item.name" :label="item.name" style="float: left;padding-left: 15px;padding-bottom:2px;"/>
        </div>

        <div class="mb-1" style="height: 500px;overflow: auto;font-size:10px;clear: left;">
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
      test: true,
      isBusy: false,
      items: [],
      fields: ["spotter","dxcc","country","continent","frequency","band","dx","dx_dxcc","dx_country","dx_continent", "comment","time_utc"],
      bands: [],
      selectedBands:[],
    }
  },
  mounted () {
      this.getBands();
      this.getClusterData();
  },
  watch: {
  },
  filters:{
  },
  computed: {
  },
  methods: {
      'getBands': function() {
          Tuxlog.webRequestAsync('GET', '/api/v1.0/tuxlog/LogBands?select=name&distinct', undefined, (response)=> {
            this.bands = response.data;
            //debugger;
          }, (response) => {
              alert('Error loading bands!')
          })
      },
      'getClusterData':  function () {
            var filter="";
            this.bands.forEach(band => {
                if(band['show_dxspots']=="1") {
                    if(filter!="") filter=filter+",";
                    filter=filter+"'"+band['name']+"'";
                }
            });

            if(filter!="") {
                filter='(band IN ('+filter+'))';
            }
            console.log(filter);

            var url='/api/v1.0/tuxlog/LogVwDxclusterSpots?pagesize=50';
            if(filter!="") {
                url=url+'&where='+filter
            }
            //console.log(url);
            Tuxlog.webRequestAsync('GET',url , undefined,(response) => {
                this.items=response.data;
                window.setTimeout(this.getClusterData, 5000);
            },(response) => { 
                alert('Error loading cluster data. Pse restart!') ;
            })
      } //fn
  }
}

</script>