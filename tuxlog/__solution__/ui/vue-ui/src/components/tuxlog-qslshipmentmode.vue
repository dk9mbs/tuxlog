<template>
    
    <div>
        <tuxlog-input class="mb-1" v-model="value['id']" label="ID" type="text" id="id" />
        <tuxlog-input class="mb-1" v-model="value['description']" label="Desc" type="text" id="id" />
    </div>

</template>

<script>
export default {
    name: 'rig',
    props:["value"]

}
</script>