<template>
  <div>
    (JSONTypeForm)
    <!-- MODEL: {{ model }}
    DATA: {{ data }} -->
    <TypeSelect v-model="data.type" @schema="schema => changeSchema(schema)" :error_messages="error_messages" :has_error="has_error" v-if="data" :disable="existing_schema !== null" :read_only="existing_schema !== null"/>
    <slot name="content" v-bind= "{ errors, has_error, model:data }">
      Override me
      Data: {{model}}
      Errors: {{errors}}
    </slot>
    <!-- JSONSchemaForm data: {{ data.data }} errors: {{ errors }} -->
    <JSONSchemaForm v-model="data.data" :schema="schema" ref="custom_fields" v-if="schema && data.data" :modify="true" :errors="errors.data" :warnings="{}">
      <template v-for="(_, name) in $slots" #[name]="slotData">
        <slot :name="name" v-bind="slotData || {}" />
      </template>
    </JSONSchemaForm>
    <slot name="buttons" v-bind:submit="submit">
      <q-btn label="Submit" color="primary" @click="submit" v-if="!hideButtons"/>
    </slot>
  </div>
</template>
<script>
import _ from 'lodash'
import TypeSelect from '../TypeSelect.vue'
import JSONSchemaForm from 'src/assets/jsonschema/components/forms/JSONSchemaForm.vue'

export default {
  props: {
    errors: { type: Object, default () { return {} } }, modelValue: { type: Object, default () { return { data: {} } } }
  },
  // emits: ['update:modelValue'],
  data () {
    return {
      schema: null,
      existing_schema: null,
      lock_type: false,
      data: this.modelValue// _.cloneDeep(this.modelValue)
    }
  },
  methods: {
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
    if (this.data) {
      if (this.data.schema) {
        this.existing_schema = this.data.schema
        this.changeSchema(this.data.schema)
      } else if (this.data.type && this.data.type.schema) {
        this.changeSchema(this.data.type.schema)
      }
    }
    console.log('JSONTypeForm', this.data, this)
  },
  components: {
    TypeSelect,
    JSONSchemaForm
  }
}
</script>
