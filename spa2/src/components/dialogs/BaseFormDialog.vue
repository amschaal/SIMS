<template>
  <BaseDialog ref="dialog" :title="title">
    <template v-slot:content>
      <component :is="formComponent" :onSuccess="success" :onError="onError" :hide-buttons="true" :model="data" ref="form" v-model="data">
        <template v-slot:buttons>Nothing here</template>
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
import _ from 'lodash'
export default {
  props: ['formComponent', 'title', 'onSuccess', 'onError', 'model', 'modelValue'],
  emits: ['update:modelValue'],
  data () {
    return {
      errors: {},
      data: this.modelValue
    }
  },
  methods: {
    open (data) {
      this.data = _.cloneDeep(data)
      this.$refs.dialog.open()
    },
    close () {
      this.$refs.dialog.close()
    },
    success (data) {
      if (this.onSuccess) {
        this.onSuccess(data)
      }
      this.close()
    },
    submit () {
      if (this.$refs.form && this.$refs.form.submit) {
        this.$refs.form.submit(response => this.$emit('update:modelValue', response.data))
      } else {
        this.$refs.form.$refs.form.submit(response => this.$emit('update:modelValue', response.data))
      }
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
