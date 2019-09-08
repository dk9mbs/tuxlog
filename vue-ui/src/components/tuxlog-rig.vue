<template>
    
    <div>
        <tuxlog-input class="mb-1" v-model="value['id']" label="ID" type="text" id="id" />
        <tuxlog-input class="mb-1" v-model="value['description']" label="Desc" type="text" id="id" />
        <tuxlog-input class="mb-1" v-model="value['hamlib_id']" label="Hamlib ID" type="number" id="id" />
        <tuxlog-input class="mb-1" v-model="value['remote_host']" label="Host" type="text" id="id" />
        <tuxlog-input class="mb-1" v-model="value['remote_port']" label="Port" type="number" id="id" />
    </div>

</template>

<script>
export default {
    name: 'rig',
    props:["value"]

}
</script>