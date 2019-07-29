<template>
  <BaseDialog ref="dialog" :title="title">
    <template v-slot:content>
      <component :is="tableComponent" :filters="filters" :options="options" ref="table"></component>
    </template>
    <template v-slot:buttons>
      <q-btn flat label="Select" color="primary" v-close-popup @click="getSelected"/>
      <q-btn flat label="Close" color="primary" v-close-popup />
    </template>
  </BaseDialog>
</template>
<script>
import BaseDialog from './BaseDialog.vue'
export default {
  props: ['tableComponent', 'title', 'options', 'filters'],
  data () {
    return {
    }
  },
  methods: {
    open () {
      console.log('open!', this.title)
      this.$refs.dialog.open()
    },
    getSelected () {
      console.log('selected', this.$refs.table.$refs.table.getSelected())
      this.$refs.dialog.close()
      // return this.$refs.dialog.getSelected()
    }
  },
  mounted: function () {

  },
  components: {
    BaseDialog
  }
}
</script>
