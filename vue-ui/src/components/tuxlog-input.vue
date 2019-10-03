<template>
<div>
      <!--
      <b-form-group
        id="fieldset-horizontal"
        label-cols-sm="0"
        label-cols-lg="5"
        v-bind:descriptio="label"
        v-bind:label="label"
        label-for="input-horizontal"
        class="my-1"
      > 
      -->
    <b-input-group size="sm" class="mb-0">

    <template v-slot:prepend>
      <b-input-group-text v-b-popover.hover.left="tooltip" :title="label"
        v-if="hidelabel === false"
        style="border-radius: 10px;background-color:silver;min-width: 70px;margin-right:3px;padding-top: 8px;padding-left:5px;font-size:10px;">
        <div v-if="mandatory!==true">{{ label }}</div>
        <div v-if="mandatory===true" >{{ label }}*</div>
        </b-input-group-text>
    </template>  

    <b-form-input v-bind:readonly="readonly" v-bind:id="id" v-bind:type="type" v-model="getValue" 
            size="sm" @input="handleInput" @change="onchange_value" class="mb-0" style="border-radius: 10px">
    </b-form-input>
    </b-input-group>
    <!-- </b-form-group> --> 
    </div>
</template>

<script>
//import func from '../../vue-temp/vue-editor-bridge';


export default {
  name: 'tuxlog-input',
  props: {value: {}, label:{default: ''},type:{default: 'text'}, id:{}, readonly: {default: false}, 
    tooltip:{default: ''}, mandatory:{default: false}, 
    hidelabel:{type: Boolean, default: false}
  },
  computed: {
    getValue: {
      get: function() {return this.value},
      set: function (t) {}
    }
  },
  methods: {
      onchange_value(e) {
        this.$emit('onchange_value', e)
      },
      handleInput (e) {
        this.$emit('input', e)
      }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.input-group-addon {
    min-width:60%;
    text-align:left;
}
</style>
