<template>
  <div>
    (JSONTypeForm)
    <!-- MODEL: {{ model }}
    DATA: {{ data }} -->
    <TypeSelect v-model="data.type" @schema="schema => changeSchema(schema)" :error_messages="error_messages" :has_error="has_error" v-if="data" :disable="existing_schema !== null" :read_only="existing_schema !== null" :emit_object="true"/>
    <slot name="content" v-bind= "{ errors, has_error, model:data }">
      Override me
      Data: {{model}}
      Errors: {{errors}}
    </slot>
    <!-- JSONSchemaForm data: {{ data.data }} errors: {{ errors }} -->
    <fieldset v-if="schema && data.data">
      <legend v-if="data.type && data.type.name">{{ data.type.name }} fields</legend>
      <JSONSchemaForm v-model="data.data" :schema="schema" ref="custom_fields" :modify="true" :errors="errors.data" :warnings="{}">
        <template v-for="(_, name) in $slots" #[name]="slotData">
          <slot :name="name" v-bind="slotData || {}" />
        </template>
      </JSONSchemaForm>
    </fieldset>
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
