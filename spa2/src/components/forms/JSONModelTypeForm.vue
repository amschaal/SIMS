<template>
  <div class="q-pa-sm q-gutter-sm">
    (JSONModelTypeForm)
    <slot name="content" v-bind:errors="error_messages" v-bind:has_error="has_error" v-bind:_errors="errors" v-bind:model="data">
      <!-- Override me
      Data: {{model}}
      Errors: {{errors}} -->
    </slot>
    <!-- <fieldset>
      <legend>Custom fields</legend>
      <CustomFields v-model="data.data" :schema="schema" ref="custom_fields" v-if="schema && data.data" :modify="true" :errors="errors.data" :warnings="{}"/>
    </fieldset> -->
    <JSONSchemaForm v-model="data" :schema="jsonschema" ref="custom_fields" v-if="jsonschema && data" :modify="true" :errors="errors" :warnings="{}" :ui="ui">
      <template #field_type="{ data }">
          <TypeSelect v-model="data.type" :emit_object="true" @schema="schema => changeSchema(schema)" :error_messages="error_messages" :has_error="has_error" v-if="data" :model-filter="modelFilter"/>
      </template>
      <!-- Pass along slots from calling template -->
      <template v-for="(_, name) in $slots" #[name]="slotData">
        <slot :name="name" v-bind="slotData || {}" />
      </template>
    </JSONSchemaForm>
    <!-- jsonschema: {{ jsonschema }}
    data: {{ data }} -->
  </div>
</template>
<script>
import _ from 'lodash'
import TypeSelect from '../TypeSelect.vue'
import JSONSchemaForm from 'src/assets/jsonschema/components/forms/JSONSchemaForm.vue'
// import CustomFields from 'src/assets/jsonschema/forms/customFields.vue'

export default {
  props: {
    errors: { type: Object, default () { return {} } },
    // schema: { type: Object, default () { return {} } },
    schemaUrl: String,
    schema: Object,
    modelFilter: String,
    // schema: {
    //   type: Object,
    //   default () {
    //     return {
    //       type: 'object',
    //       properties: {
    //         type: {
    //           type: 'string',
    //           title: 'Type'
    //         },
    //         data: {
    //           type: 'object',
    //           title: 'Data'
    //         }
    //       }
    //     }
    //   }
    // },
    modelValue: { type: Object, default () { return {} } },
    exclude: { type: Array, default () { return [] } },
    ui: { type: Object, default () { return {} } }
  },
  emits: ['update:modelValue'],
  data () {
    return {
      // jsonschema: this.schema,
      // model: { data: { foo: 'baz' }, type: 'machine_illumina_hiseq' }
      data: this.modelValue, // _.cloneDeep(this.modelValue)
      type_schema: null,
      api_schema: null
    }
  },
  methods: {
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
        return this._schema
      }
      const schema = _.cloneDeep(this._schema)
      schema.properties.data = this.type_schema
      schema.properties.data.type = 'object'
      schema.properties.data.title = this.data.type.name
      console.log('jsonschema', schema)
      return schema
    },
    _schema: function () {
      return this.schema || this.api_schema
    }
  },
  mounted: function () {
    if (this.data && !this.data.data) {
      this.data.data = {}
    }
    console.log('JSONForm', this)
    if (this.schemaUrl) {
      this.$api
        .get(this.schemaUrl)
        .then(response => {
          this.api_schema = response.data
        })
    }
  },
  components: {
    TypeSelect,
    JSONSchemaForm
    // CustomFields
    // BaseDialog
  }
}
</script>
