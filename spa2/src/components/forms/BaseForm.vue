<template>
  <div class="q-pa-sm q-gutter-sm">
    <slot name="content" v-bind:errors="error_messages" v-bind:has_error="has_error" v-bind:_errors="errors" v-bind:model="model">
      Override me
      Data: {{model}}
      Errors: {{errors}}
    </slot>
    <slot name="buttons" v-bind:submit="submit">
      <q-btn label="Submit" color="primary" @click="submit"/>
    </slot>
  </div>
</template>
<script>
import _ from 'lodash'
export default {
  props: ['modelValue', 'apiUrl', 'apiMethod', 'onSuccess', 'onError'],
  emits: ['update:modelValue'],
  data () {
    return {
      errors: {},
      model: this.modelValue
    }
  },
  methods: {
    submit () {
      const self = this
      this.$api[this.apiMethod](this.apiUrl, this.model)
        .then(function (response) {
          console.log('success', response)
          self.errors = {}
          if (self.onSuccess) {
            self.onSuccess(response)
          }
        })
        .catch(function (error) {
          if (error.response && error.response.data) {
            self.errors = error.response.data
            console.log('errors', error.response.data, self.errors)
            if (self.onError) {
              self.onError(error)
            }
          }
        })
    }
  },
  computed: {
    error_messages: function () {
      return _.mapValues(this.errors, function (e) { return Array.isArray(e) ? e.join(',') : '' })
    },
    has_error: function () {
      return _.mapValues(this.errors, function (e) { return e !== undefined })
      // return _.mapValues(this.errors, function (e) { return Array.isArray(e) })
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
