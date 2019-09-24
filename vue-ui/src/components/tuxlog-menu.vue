<template>
  <span>
    <!--<div class="example-description">
      <input type="text" placeholder="Type to filter..." v-model="filter" class="filter-field">
    </div>-->
    <div class="example-tree">
    <tree :data="items" :filter="filter" :options="opts" ref="tree">
        <div slot-scope="{ node }">
          <div @click="test(node);">{{ node.text }}</div>
          <!--   class="node-container"  class="node-text"   
          <div class="node-controls">
            <a href="#" @mouseup.stop="alert(node.text);">{{ node.text }}</a>
            <a href="#" @mouseup.stop="editNode(node)">Edit</a>
            <a href="#" @mouseup.stop="removeNode(node)">Remove</a>
            <a href="#" @mouseup.stop="addChildNode(node)">Add child</a>
          </div>
          -->
        </div>
      </tree>
    </div>
  </span>
</template>

<script>
    //https://github.com/amsik/liquor-tree/blob/master/demo/pages/events.html
    export default {
      data() {
        return {
          items: [
            {text: 'QSO', id: '/ui/qso'},
            {text: 'Reporting', id: '/ui'},
            {text: 'Basedata', id: '/ui', children: [
              {text: 'Rigs', id: '/ui/dataview/LogRigs/default'},
              {text: 'Modes', id: '/ui/dataview/LogModes/default'},
              {text: 'Logbooks', id: '/ui/dataview/LogLogbooks/default'},
              {text: 'QSL shipment', id: '/ui/dataview/LogQslshipmentmodes/default'},
            ]}
          ],
        }
      },
      filter: null,
      opts: {
        checkbox: true,
        filter: {
          plainList: false
        },
        dnd: true
      },
      methods: {
        test: function(node) {
          this.$emit('onClickNode', node)
        }
      }
      
    }
</script>

<style scoped>
    .filter-field {
      display: block;
      width: 100%;
      padding: 3px;
    }
    .node-controls a {
      color: #ff14ce
    }
</style>
