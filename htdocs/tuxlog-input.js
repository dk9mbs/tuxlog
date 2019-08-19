import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.10/dist/vue.esm.browser.js'

hallo=new Vue();

var test = {
    props: ["label","value", "type", "id", "readonly"],
    template: '<div style="margin-top:0px;">\
      <b-form-group\
        id="fieldset-horizontal"\
        label-cols-sm="0"\
        label-cols-lg="0"\
        v-bind:description="label"\
        v-bind:lab="label"\
        label-for="input-horizontal"\
      >\
    <b-form-input v-bind:readonly="readonly" v-bind:id="id" v-bind:type="type" v-model="value" size="sm" @input="handleInput" @change="onchange_value"></b-form-input>\
    </b-form-group>\
    </div>',
  
    methods: {
      onchange_value(e) {
        this.$emit('onchange_value', e)
      },
      handleInput (e) {
        this.$emit('input', this.value)
      }
    }
  }

export default {test}