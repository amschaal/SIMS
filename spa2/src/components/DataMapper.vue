<template>
  <div>
    <template v-for="related in related_types" :key="related.model">
      <div>
        <h5>Map {{related.title}}</h5>
        <TypeSelect v-model="mapping[related.model].type" :error_messages="{}" :has_error="false" :model-filter="related.model" @update:model-value="val => updateRelatedSchema(related.model, val)"/><br>
        <q-markup-table flat bordered dense>
        <thead>
          <tr><th colspan="4">{{related.title}}</th></tr>
          <tr><th colspan="2">Destination</th><th colspan="2">Source</th></tr>
        </thead>
        <tbody>
          <tr v-if="mapping[related.model]">
            <td colspan="2" style="width: 50%;">
            </td>
            <td colspan="2" style="width: 50%;">
                <q-select
                  label="Submission Table"
                  :options="tables"
                  v-model="mapping[related.model].source"
                  dense
                  outlined
                  option-value="id"
                  option-label="label"
                  emit-value
                  v-if="mapping[related.model].source != '.'"
                  />

            </td>
          </tr>
          <tr v-if="mapping[related.model] && mapping[related.model].source && mapping[related.model].type && related_schemas[related.model]">
            <td colspan="4" >
              <TableMapper :source-schema="submission_type.submission_schema" :dest-schema="related_schemas[related.model]" :key="related.model+'_'+mapping[related.model].type" v-model="mapping[related.model].mapping" :table="mapping[related.model].source" :model="related.model"/>
            </td>
          </tr>
        </tbody>
      </q-markup-table>
      {{ mapping }}
      </div>
    </template>
  </div>
</template>

<style>
</style>

<script>
import TableMapper from './TableMapper.vue'
import TypeSelect from 'src/components/TypeSelect.vue'
import ModelSchemas from 'src/model_schemas/schemas'

export default {
  props: ['submission_type', 'type', 'modelValue'],
  emits: ['update:modelValue'],
  data () {
    return {
      mapping: this.modelValue,
      related_types: [{ model: 'project', title: 'Project', source: '.' }, { model: 'sample', accessor: 'samples', title: 'Samples' }, { model: 'pool', accessor: 'pools', title: 'Pools' }],
      related_schemas: {}
    }
  },
  mounted () {
    if (!this.mapping.project) {
      this.mapping.project = { type: null, mapping: {}, source: '.' }
    }
    this.related_types.forEach(r => {
      if (!this.mapping[r.model]) {
        this.mapping[r.model] = { type: 'array', source: null, mapping: {} }
      }
    })
  },
  methods: {
    getAvailableFields (schema, variableType) {
      const fieldTypes = variableType === 'array' ? ['array'] : ['number', 'string']
      return schema.order.filter(v => (!fieldTypes || fieldTypes.indexOf(schema.properties[v].type) !== -1))
    },
    getOptions (schema, mapping, variableType) {
      if (!schema) {
        return []
      }
      return this.getAvailableFields(schema, variableType).map(v => ({ id: v, label: schema.properties[v].title || v }))
    },
    getModelSchema (model, type) {
      return ModelSchemas.getSchema(model, type)
    },
    updateRelatedSchema (model, type) {
      this.related_schemas[model] = ModelSchemas.getSchema(model, type)
    }
  },
  computed: {
    tables () {
      const schema = this.submission_type.submission_schema
      const order = schema.order.filter(f => (schema.properties[f].type) === 'array')
      return order.map(f => ({ id: f, label: schema.properties[f].title ? `${schema.properties[f].title} (${f})` : f }))
    }
  },
  watch: {
    modelValue: function (val) {
      console.log('JSONMapper model value changed ', val)
      this.mapping = val
    }
  },
  components: { TableMapper, TypeSelect }
}
</script>
