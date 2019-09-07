<template>
<div>
  <!--
  <b-form-group
        id="fieldset-horizontal"
        label-cols-sm="0"
        label-cols-lg="0"
        v-bind:description="label"
        v-bind:lab="label"
        label-for="input-horizontal"
      >
      -->
    <b-input-group size="sm" class="mb-0">

    <template v-slot:prepend>
      <b-input-group-text 
        style="border-radius: 25px;background-color:silver;min-width: 70px;margin-right:3px;padding-top: 8px;padding-left:5px;font-size:10px;">
        <div>{{ label }}</div>
        </b-input-group-text>
    </template>  

  <b-form-select v-bind:disabled="readonly" v-bind:id="id" v-model="value" class="mb-0" size="sm" 
        @input="handleInput" @change="onchange_value" style="border-radius: 25px">
  <option v-bind:key="n" v-for="n in values" v-bind:value="n.id">{% raw %}{{ n.description }}{% endraw %}</option>
  </b-form-select>
  
  </b-input-group>  
  <!--</b-form-group> -->
  </div>
</template>

<script>
export default {
  name: 'tuxlog-option',
  props: ["values", "value", "label", "id", "readonly"],
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

</style>
