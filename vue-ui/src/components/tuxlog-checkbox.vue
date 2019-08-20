<template>
<div><label for="logbook_id" size="sm">{% raw %}{{ label }}{% endraw %}
    <b-form-checkbox v-bind:id="id" unchecked-value="0" value="1" v-model="value" size="sm" @input="handleInput"></b-form-checkbox>
  </label></div>
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
