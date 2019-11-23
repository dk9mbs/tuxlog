<template>
    
    <div>
        <tuxlog-input class="mb-1" v-model="value['id']" label="ID" type="text" id="id" />
        <tuxlog-input class="mb-1" v-model="value['description']" label="Desc" type="text" id="description" />
        <tuxlog-input class="mb-1" v-model="value['mycall']" label="Call" type="text" id="mycall" />
        <tuxlog-input class="mb-1" v-model="value['parent']" label="Parent" type="text" id="parent" />
        <tuxlog-checkbox class="mb-1" v-model="value['deleted']" label="Inactive" id="deleted" />

    </div>

</template>

<script>
export default {
    name: 'rig',
    props:["value"]

}
</script>