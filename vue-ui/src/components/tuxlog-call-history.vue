<template>
<div>
    <div  v-if="pending===true" class="d-flex justify-content-center mb-3">
            <b-spinner label="Loading..."></b-spinner>
        </div>
        <b-table v-if="pending===false"
          striped hover small
          v-bind:bordered="true" v-bind:items="items" v-bind:fields="fields" @row-clicked="handleClick">
        </b-table>
  </div>
</template>

<script>
export default {
  name: 'tuxlog-call-history',
  props: ["fields", "items", "id", "pending"],
  methods: {
      handleClick (record, index) {
        this.$emit('onclick_row', record, index)
      }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
