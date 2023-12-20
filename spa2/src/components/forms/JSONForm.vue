<template>
  <div class="q-pa-sm q-gutter-sm">
    <!-- MODEL: {{ model }}
    DATA: {{ data }} -->
    <TypeSelect v-model="data.type" @schema="schema => changeSchema(schema)" :error_messages="error_messages" :has_error="has_error" v-if="data"/>
    <slot name="content" v-bind:errors="error_messages" v-bind:has_error="has_error" v-bind:_errors="errors" v-bind:model="model">
      Override me
      Data: {{model}}
      Errors: {{errors}}
    </slot>
    <fieldset>
      <legend>Custom fields</legend>
      <CustomFields v-model="data.data" :schema="schema" ref="custom_fields" v-if="schema && data.data" :modify="true" :errors="errors.data" :warnings="{}"/>
    </fieldset>
    <slot name="buttons" v-bind:submit="submit">
      <q-btn label="Submit" color="primary" @click="submit" v-if="!hideButtons"/>
    </slot>
  </div>
</template>
<script>
import _ from 'lodash'
import TypeSelect from '../TypeSelect.vue'
import CustomFields from 'src/assets/jsonschema/forms/customFields.vue'

export default {
  props: ['apiUrl', 'apiMethod', 'onSuccess', 'onError', 'hideButtons', 'model'],
  data () {
    return {
      errors: {},
      schema: {},
      // model: { data: { foo: 'baz' }, type: 'machine_illumina_hiseq' }
      data: this.model
    }
  },
  methods: {
    submit () {
      const self = this
      this.$api[this.apiMethod](this.apiUrl, this.data)
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
            self.errors = error.response.data
            console.log('errors', error.response.data, self.errors)
            if (self.onError) {
              self.onError(error)
            }
          }
        })
    },
    changeSchema (schema) {
      this.schema = schema
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
  mounted: function () {
    if (this.data && !this.data.data) {
      this.data.data = {}
    }
  },
  components: {
    TypeSelect,
    CustomFields
    // BaseDialog
  }
}
</script>
