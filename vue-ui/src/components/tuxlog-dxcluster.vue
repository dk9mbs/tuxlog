<template>
    
    <div>
        <tuxlog-input class="mb-1" v-model="value['id']" label="ID" type="text" id="id" />
        <tuxlog-input class="mb-1" v-model="value['host']" label="Host" type="text" id="id" />
        <tuxlog-input class="mb-1" v-model="value['port']" label="Port" type="number" id="id" />
        <tuxlog-input class="mb-1" v-model="value['prompt_username']" label="Prompt (user)" type="text" id="id" />
        <tuxlog-input class="mb-1" v-model="value['username']" label="Username" type="text" id="id" />
        <tuxlog-input class="mb-1" v-model="value['prompt_password']" label="Prompt (pwd)" type="text" id="id" />
        <tuxlog-input class="mb-1" v-model="value['password']" label="Password" type="text" id="id" />
        <tuxlog-input class="mb-1" v-model="value['position']" label="Position" type="number" id="id" />


    </div>

</template>

<script>
export default {
    name: 'rig',
    props:["value"]

}
</script>