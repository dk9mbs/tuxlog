<template>
<div>
  <!--<label for="logbook_id" size="sm">{% raw %}{{ label }}{% endraw %}-->
    <b-input-group size="sm" class="mb-0">

    <template v-slot:prepend>
      <b-input-group-text 
        style="border-radius: 25px;background-color:silver;min-width: 70px;margin-right:3px;padding-top: 8px;padding-left:5px;font-size:10px;">
        <div>{% raw %}{{ label }}{% endraw %}</div>
        </b-input-group-text>
    </template>  

    <b-form-checkbox v-bind:id="id" unchecked-value="0" value="1" v-model="value" size="sm" @input="handleInput" switch></b-form-checkbox>

  </b-input-group>
  <!--</label>-->
  
  </div>
</template>

<script>
export default {
  name: 'tuxlog-checkbox',
  props: ["value", "label", "id"],
  methods: {
      handleInput (e) {
        this.$emit('input', e)
      }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
