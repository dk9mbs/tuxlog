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
        style="border-radius: 25px;background-color:silver;min-width: 70px;margin-right:3px;padding-top: 8px;padding-left:5px;font-size:10px;">
        <div v-if="mandatory!==true">{% raw %}{{ label }}{% endraw %}</div>
        <div v-if="mandatory===true" >{% raw %}{{ label }}*{% endraw %}</div>
        </b-input-group-text>
    </template>  

    <b-form-input v-bind:readonly="readonly" v-bind:id="id" v-bind:type="type" v-model="value" 
            size="sm" @input="handleInput" @change="onchange_value" class="mb-0" style="border-radius: 25px">
    </b-form-input>
    </b-input-group>
    <!-- </b-form-group> --> 
    </div>
</template>

<script>


export default {
  name: 'tuxlog-input',
  props: ["label","value", "type", "id", "readonly","tooltip", "mandatory"],
  methods: {
      onchange_value(e) {
        this.$emit('onchange_value', e)
      },
      handleInput (e) {
        this.$emit('input', this.value)
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
