<template>
<span>


    <b-button pill 
      variant="outline-secondary" v-on:click="handleClick()" size="sm"
      v-bind:disabled="readonly"
    >{{ label }}
    </b-button>


    </span>
</template>

<script>


export default {
  name: 'tuxlog-input',
  props: ["label","value", "type", "id", "readonly", "tooltip"],
  methods: {
      handleClick (e) {
        this.$emit('click', e)
        this.$emit('onclick', e)
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
