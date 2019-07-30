<template>
  <BaseDialog ref="dialog" :title="title">
    <template v-slot:content>
      <slot name="content" v-bind:errors="error_messages" v-bind:has_error="has_error" v-bind:data="data"></slot>
      Data: {{data}}
      Errors: {{errors}}
    </template>
    <template v-slot:buttons>
      <q-btn flat label="Submit" color="primary" @click="submit"/>
      <q-btn flat label="Cancel" color="primary" v-close-popup />
    </template>
  </BaseDialog>
</template>
<script>
import BaseDialog from './BaseDialog.vue'
import Vue from 'vue'
import _ from 'lodash'
export default {
  props: ['model', 'apiUrl', 'title', 'apiMethod', 'onSuccess', 'onError'],
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
      var self = this
      this.$axios[this.apiMethod](this.apiUrl, this.data)
        .then(function (response) {
          console.log('success', response)
          if (self.onSuccess) {
            self.onSuccess(response)
          }
          this.$refs.dialog.close()
        })
        .catch(function (error) {
          if (error.response && error.response.data) {
            Vue.set(self, 'errors', error.response.data)
          }
        })
    }
  },
  computed: {
    error_messages: function () {
      return _.mapValues(this.errors, function (e) { return e ? e.join(',') : '' })
    },
    has_error: function () {
      return _.mapValues(this.errors, function (e) { return e !== undefined })
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
