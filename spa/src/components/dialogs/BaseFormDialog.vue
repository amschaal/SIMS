<template>
  <BaseDialog ref="dialog" :title="title">
    <template v-slot:content>
      <component :is="formComponent" :onSuccess="onSuccess" :onError="onError" :hide-buttons="true" ref="form">
        <template v-slot:buttons>Nothing here</template>Dood
      </component>
    </template>
    <template v-slot:buttons>
      <q-btn label="Submit" color="primary" @click="submit"/>
      <q-btn label="Cancel" color="negative" v-close-popup />
    </template>
  </BaseDialog>
</template>
<script>
import BaseDialog from './BaseDialog.vue'
// import Vue from 'vue'
// import _ from 'lodash'
export default {
  props: ['formComponent', 'title', 'onSuccess', 'onError'],
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
      this.$refs.form.$refs.form.submit()
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
