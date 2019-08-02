<template>
  <div class="q-pa-sm q-gutter-sm">
    <slot name="content" v-bind:errors="error_messages" v-bind:has_error="has_error" v-bind:_errors="errors" v-bind:model="model">
      Override me
      Data: {{model}}
      Errors: {{errors}}
    </slot>
    <slot name="buttons" v-bind:submit="submit">
      <q-btn label="Submit" color="primary" @click="submit" v-if="!hideButtons"/>
    </slot>
  </div>
</template>
<script>
import Vue from 'vue'
import _ from 'lodash'
export default {
  props: ['model', 'apiUrl', 'apiMethod', 'onSuccess', 'onError', 'hideButtons'],
  data () {
    return {
      errors: {}
      // data: this.model
    }
  },
  methods: {
    submit () {
      var self = this
      this.$axios[this.apiMethod](this.apiUrl, this.model)
        .then(function (response) {
          console.log('success', response)
          self.errors = {}
          if (self.onSuccess) {
            self.onSuccess(response)
          }
          this.$refs.dialog.close()
        })
        .catch(function (error) {
          if (error.response && error.response.data) {
            Vue.set(self, 'errors', error.response.data)
            if (self.onError) {
              self.onError(error)
            }
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
    // BaseDialog
  }
}
</script>
