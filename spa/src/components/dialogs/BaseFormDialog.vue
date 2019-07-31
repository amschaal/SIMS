<template>
  <BaseDialog ref="dialog" :title="title">
    <template v-slot:content>
      {{formComponent}}Foo!
      <component :is="formComponent" ref="form">
        <template v-slot:buttons></template>
      </component>
    </template>
    <template v-slot:buttons>
      <q-btn flat label="Submit" color="primary" @click="submit"/>
      <q-btn flat label="Cancel" color="primary" v-close-popup />
    </template>
  </BaseDialog>
</template>
<script>
import BaseDialog from './BaseDialog.vue'
// import Vue from 'vue'
// import _ from 'lodash'
export default {
  props: ['formComponent', 'title'],
  data () {
    return {
      errors: {},
      data: this.model
    }
  },
  methods: {
    open () {
      this.$refs.dialog.open()
    },
    submit () {
      this.$refs.form.submit()
    }
  },
  // mounted: function () {
  //
  // },
  components: {
    BaseDialog
  }
}
</script>
