<template>
  <BaseDialog ref="dialog" :title="title">
    <template v-slot:content>
      <component :is="tableComponent" :filters="filters" :options="options" ref="table" @selected="onSelect"></component>
    </template>
    <template v-slot:buttons>
      <q-btn flat label="Select" color="primary" v-close-popup @click="getSelected" :disable="selected === null || selected.length === 0"/>
      <q-btn flat label="Close" color="primary" v-close-popup />
    </template>
  </BaseDialog>
</template>
<script>
import BaseDialog from './BaseDialog.vue'
export default {
  props: ['tableComponent', 'title', 'options', 'filters'],
  emits: ['selected'],
  data () {
    return {
      selected: null
    }
  },
  methods: {
    open () {
      this.$refs.dialog.open()
    },
    onSelect (val) {
      this.selected = val
    },
    getSelected () {
      this.$emit('selected', this.selected)
      this.$refs.dialog.close()
    }
  },
  mounted: function () {

  },
  components: {
    BaseDialog
  }
}
</script>
