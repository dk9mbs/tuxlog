<template>
<div>
  <!--<label for="logbook_id" size="sm">{% raw %}{{ label }}{% endraw %}-->
    <b-input-group size="sm" class="mb-0">

    <template v-slot:prepend>
      <b-input-group-text  v-b-popover.hover.left="tooltip" :title="label"
        v-if="hidelabel === false"
        style="border-radius: 10px;background-color:silver;min-width: 70px;margin-right:3px;padding-top: 8px;padding-left:5px;font-size:10px;">
        <div v-if="mandatory!==true">{{ label }}</div>
        <div v-if="mandatory===true" >{{ label }}*</div>

        </b-input-group-text>
    </template>  

    <b-form-checkbox v-bind:id="id" unchecked-value="0" value="1" v-model="getValue" size="sm" @input="handleInput" switch></b-form-checkbox>

  </b-input-group>
  <!--</label>-->
  
  </div>
</template>

<script>
export default {
  name: 'tuxlog-checkbox',
  props: {value: {}, label:{default: ''}, id:{}, 
    tooltip:{default: ''}, mandatory:{default: true}, 
    hidelabel:{type: Boolean, default: false}},
  computed: {
    getValue: {
      get: function() {return this.value},
      set: function(newValue) {}
    }
  },
  methods: {
      handleInput (e) {
        this.$emit('input', e);
        this.$emit('onchange_value', e);
      }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
