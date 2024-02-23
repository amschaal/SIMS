<template>
  <div class="q-pa-sm q-gutter-sm">
    <!-- MODEL: {{ model }}
    DATA: {{ data }} -->
    <slot name="content" v-bind:errors="error_messages" v-bind:has_error="has_error" v-bind:_errors="errors" v-bind:model="data">
      Override me
      Data: {{model}}
      Errors: {{errors}}
    </slot>
    <!-- <fieldset>
      <legend>Custom fields</legend>
      <CustomFields v-model="data.data" :schema="schema" ref="custom_fields" v-if="schema && data.data" :modify="true" :errors="errors.data" :warnings="{}"/>
    </fieldset> -->
    <JSONSchemaForm v-model="data" :schema="jsonschema" ref="custom_fields" v-if="jsonschema && data" :modify="true" :errors="errors" :warnings="{}">
      <template #field_type="{ data }">
          <TypeSelect v-model="data.type" emit_object @schema="schema => changeSchema(schema)" :error_messages="error_messages" :has_error="has_error" v-if="data"/>
      </template>
      <!-- Pass along slots from calling template -->
      <template v-for="(_, name) in $slots" #[name]="slotData">
        <slot :name="name" v-bind="slotData || {}" />
      </template>
    </JSONSchemaForm>
    jsonschema: {{ jsonschema }}
    data: {{ data }}
    <slot name="buttons" v-bind:submit="submit">
      <q-btn label="Submit" color="primary" @click="submit" v-if="!hideButtons"/>
    </slot>
  </div>
</template>
<script>
import _ from 'lodash'
import TypeSelect from '../TypeSelect.vue'
import JSONSchemaForm from 'src/assets/jsonschema/forms/JSONSchemaForm.vue'
// import CustomFields from 'src/assets/jsonschema/forms/customFields.vue'

export default {
  props: {
    apiUrl: String,
    apiMethod: String,
    onSuccess: Function,
    onError: Function,
    hideButtons: Boolean,
    schema: { type: Object, default () { return {} } },
    modelValue: { type: Object, default () { return {} } },
    exclude: { type: Array, default () { return [] } }
  },
  emits: ['update:modelValue'],
  data () {
    return {
      errors: {},
      // jsonschema: this.schema,
      // model: { data: { foo: 'baz' }, type: 'machine_illumina_hiseq' }
      data: this.modelValue, // _.cloneDeep(this.modelValue)
      type_schema: null
    }
  },
  methods: {
    submit (onSuccess) {
      const self = this
      this.$api[this.apiMethod](this.apiUrl, this.data)
        .then(function (response) {
          console.log('success', response.data)
          self.$emit('update:modelValue', response.data)
          self.errors = {}
          if (self.onSuccess) {
            self.onSuccess(response)
          }
          if (onSuccess) {
            onSuccess(response)
          }
          this.$parent.$parent.$refs.dialog.close()
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
      console.log('changeSchema!', schema)
      this.type_schema = schema
    }
  },
  computed: {
    error_messages: function () {
      return _.mapValues(this.errors, function (e) { return Array.isArray(e) ? e.join(',') : '' })
    },
    has_error: function () {
      return _.mapValues(this.errors, function (e) { return e !== undefined })
      // return _.mapValues(this.errors, function (e) { return Array.isArray(e) })
    },
    jsonschema: function () {
      console.log('jsonschema!!!!')
      if (!this.type_schema) {
        return this.schema
      }
      const schema = _.cloneDeep(this.schema)
      schema.properties.data = this.type_schema
      schema.properties.data.type = 'object'
      schema.properties.data.title = this.data.type.name
      console.log('jsonschema', schema)
      return schema
    }
  },
  mounted: function () {
    if (this.data && !this.data.data) {
      this.data.data = {}
    }
    console.log('JSONForm', this)
  },
  components: {
    TypeSelect,
    JSONSchemaForm
    // CustomFields
    // BaseDialog
  }
}
</script>
