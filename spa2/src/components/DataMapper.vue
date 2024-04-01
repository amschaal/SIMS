<template>
  <div>
    <q-markup-table flat bordered dense>
      <thead>
        <tr><th colspan="3">Destination</th><th colspan="3">Source <q-btn label="I'm feeling lucky!" v-on:click="autoAssign()"></q-btn></th></tr>
        <tr>
          <th class="text-left" style="width: 10%;">Destination Variable</th>
          <th class="text-left">Type</th>
          <th class="text-left">Name</th>
          <th class="text-left">Source Variable</th>
          <th class="text-left">Type</th>
          <th class="text-left">Name</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="variable in schema_to_variables(type.schema)" :key="variable">
        <tr v-if="type.schema.properties[variable].type === 'array'">
          <td class="text-left" style="width: 10%;">{{variable}}</td>
          <td class="text-left">{{type.schema.properties[variable].type}}</td>
          <td class="text-left">{{type.schema.properties[variable].title}}</td>
          <td colspan="3">
            Choose Table
            <!-- {{mapping[variable]}}
            <q-select dense outlined v-model="mapping_type[variable]" :options="mapping_types" label="Select Mapping Type"
                option-value="id"
                option-label="label"
                @update:modelValue="val => selectMappingType(val, variable)"
                >
                <template v-slot:after v-if="mapping[variable]">
                  <q-btn @click="clearTableVariable(variable)" round icon="delete"></q-btn>
                </template>
            </q-select>
              <TypeSelect :dense="true" :error_messages="{}" :has_error="{}" :modelValue="mapping[variable].model_type" @update:model-value="val => selectedModelType(val, variable)" :emit_object="true" v-if="mapping[variable] && mapping[variable].mapping_type === 'model'" :model-filter="mapping[variable].model"/> -->
          </td>
        </tr>
        <tr v-else>
          <td class="text-left" style="width: 10%;">{{variable}}</td>
          <td class="text-left">{{type.schema.properties[variable].type}}</td>
          <td class="text-left">{{type.schema.properties[variable].title}}</td>
          <td>
            <q-select dense outlined v-model="mapping[variable]" :options="getOptions(submission_type.submission_schema, type.schema.properties[variable].type)" label="Select Variable"
                option-value="id"
                option-label="label"
                emit-value
                @update:modelValue="val => selected(val, variable)"
                >
                <template v-slot:after v-if="mapping[variable]">
                  <q-btn @click="clearVariable(variable)" round icon="delete"></q-btn>
                </template>
                </q-select>
          </td>
          <td><span v-if="mapping[variable]">{{submission_type.submission_schema.properties[mapping[variable]].type}}</span></td>
          <td><span v-if="mapping[variable]">{{submission_type.submission_schema.properties[mapping[variable]].title}}</span></td>
        </tr>
        <tr v-if="mapping[variable] && mapping[variable].mapping && variable_schemas[variable]">
          <td>
            Map table variables here....
          </td>
          <td colspan="5" >
            <!-- <JSONTableMapper :source-schema="submission_type.submission_schema.properties[variable].schema" :dest-schema="type.schema.properties[mapping[variable].variable].schema" v-model="mapping[variable].mapping"/> -->
            <!-- <TableMapper :source-schema="submission_type.submission_schema.properties[variable].schema" :dest-schema="variable_schemas[variable]" v-model="mapping[variable].mapping" /> -->
          </td>
        </tr>
      </template>
      </tbody>
      <!-- {{ type }} -->
    </q-markup-table>
    <h4>Mapping Pools and Samples</h4>
    <template v-for="related in related_types" :key="related.model">
      <q-markup-table flat bordered dense>
        <thead>
          <tr><th colspan="4">Samples</th></tr>
          <tr><th colspan="2">Destination</th><th colspan="2">Source</th></tr>
        </thead>
        <tbody>
          <tr>
            <td colspan="2" style="width: 50%;">
                <!-- {{ related.title }} -->
                <!-- {{ $store.jsonschema.typeSchemas[type.metadata[related.model]] }} -->
                <!-- <TypeSelect dense outlined :error_messages="{}" :has_error="{}" :modelValue="type.metadata[related.model]" @update:model-value="val => selectedModelType(val, related)" :emit_object="true" :model-filter="related.model"/> -->
            </td>
            <td colspan="2" style="width: 50%;">
              <!-- {{ type.metadata[related.model] }} -->
                <q-select label="Submission Table" :options="tables" v-model="related.source" dense outlined/>
            </td>
                <!-- <JSONTableMapper :source-schema="submission_type.submission_schema.properties[variable].schema" :dest-schema="type.schema.properties[mapping[variable].variable].schema" v-model="mapping[variable].mapping"/> -->
              <!-- <TableMapper :source-schema="submission_type.submission_schema.properties[variable].schema" :dest-schema="variable_schemas[variable]" v-model="mapping[variable].mapping" /> -->
          </tr>
          <tr>
            <td colspan="4" v-if="type.metadata[related.model] && related.source">
              <!-- {{ $store.jsonschema.typeSchemas[type.metadata[related.model]] }} -->
              {{ getModelSchema('sample', type.metadata[related.model] ) }}
              Test: <TableMapper :source-schema="submission_type.submission_schema" :dest-schema="getModelSchema('sample', type.metadata[related.model] )" v-model="mapping[related.model]" :table="related.source" :model="related.model"/>
              <p>variable_schemas: {{ variable_schemas }}</p>
            </td>
          </tr>
        </tbody>
      </q-markup-table>
    </template>
  </div>
</template>

<style>
</style>

<script>
import TableMapper from './TableMapper.vue'
// import TypeSelect from 'src/components/TypeSelect.vue'
import ModelSchemas from 'src/model_schemas/schemas'
// import SubmissionTypeSelect from 'src/components/SubmissionTypeSelect.vue'
// import TypeSelect from 'src/components/TypeSelect.vue'

export default {
  props: ['submission_type', 'type', 'modelValue'],
  emits: ['update:modelValue'],
  data () {
    return {
      mapping: this.modelValue,
      mapping_type: {},
      variable_schemas: {},
      mapping_types: [{ id: 'JSON', label: 'JSON' }, { id: 'samples', model: 'sample', label: 'Samples', schema_url: '/api/samples/jsonschema/' }, { id: 'pools', model: 'pool', label: 'Pools', schema_url: '/api/pools/jsonschema/' }],
      related_types: [{ model: 'sample', accessor: 'samples', title: 'Samples' }]
    }
  },
  mounted () {
    this.related_types.forEach(r => {
      if (!this.mapping[r.model]) {
        this.mapping[r.model] = {}
      }
    })
  },
  methods: {
    schema_to_variables (schema, path) {
      return schema.order
    },
    getAvailableFields (schema, variableType) {
      const fieldTypes = variableType === 'table' ? ['table'] : ['number', 'string']
      return schema.order.filter(v => (!fieldTypes || fieldTypes.indexOf(schema.properties[v].type) !== -1))
    },
    getOptions (schema, mapping, variableType) {
      if (!schema) {
        return []
      }
      return this.getAvailableFields(schema, variableType).map(v => ({ id: v, label: schema.properties[v].title || v }))
    },
    selected (val, variable) {
      // if (this.submission_type.submission_schema.properties[variable].type === 'table') {
      //   console.log('selected: overwriting mapping')
      //   this.mapping[variable] = { variable: val, mapping: {} }
      // }
      // console.log(val, variable, this.type.schema.properties, this.mapping[variable].variable)
      this.$emit('update:modelValue', this.mapping)
    },
    selectMappingType (val, variable) {
      console.log('selectMappingType', val, variable)
      if (val.id === 'JSON') {
        console.log('selectMappingType: overwriting mapping')
        this.mapping[variable] = { variable: val.id, mapping_type: 'JSON', mapping: {} }
      } else {
        console.log('selectMappingType: overwriting mapping')
        this.mapping[variable] = { variable: val.id, mapping_type: 'model', model: val.model, model_type: null, mapping: {} }
      }
      // if (this.submission_type.submission_schema.properties[variable].type === 'table') {
      //   this.mapping[variable] = { variable: val, mapping: {} }
      // }
      // // console.log(val, variable, this.type.schema.properties, this.mapping[variable].variable)
      this.$emit('update:modelValue', this.mapping)
    },
    selectedSchema (type, variable) {
      console.log('selectedSchema', type, variable)
      // this.mapping[variable].model_type = type.id
      this.variable_schemas[variable] = type.schema
      // alert(JSON.stringify(this.mapping[variable]))
      // this.$emit('update:modelValue', this.mapping)
    },
    selectedModelType (type, related) {
      console.log('selectedModelType', type, related)
      related.type = type
      // console.log(`/api/${this.mapping[variable].model}/jsonschema/`)
      // this.$api.post(`/api/${this.mapping[variable].model}/jsonschema/`, { type: type.id })
      // Object.getOwnPropertyNames(this.mapping[variable].mapping).forEach(prop => delete this.mapping[variable].mapping[prop])
      // this.mapping[variable].mapping = {}
      // if (this.mapping[variable] && this.mapping[variable].model_type !== type.id) {
      //   console.log('selectModelType clear mapping')
      //   Object.getOwnPropertyNames(this.mapping[variable].mapping).forEach(prop => delete this.mapping[variable].mapping[prop])
      // }
      // this.mapping[variable].model_type = type.id
      // this.variable_schemas[variable] = type.schema
      // // alert(JSON.stringify(this.mapping[variable]))
      // this.$emit('update:modelValue', this.mapping)
    },
    autoAssign () {
      const destVariables = this.schema_to_variables(this.type.schema)
      this.schema_to_variables(this.submission_type.submission_schema).forEach(variable => {
        console.log(variable)
        if (!this.mapping[variable] && destVariables.indexOf(variable) !== -1) {
          console.log('assign', variable)
          this.mapping[variable] = variable
          this.selected(variable, variable)
        }
      })
    },
    clearVariable (variable) {
      delete this.mapping[variable]
    },
    clearTableVariable (variable) {
      delete this.mapping[variable]
    },
    getModelSchema (model, type) {
      return ModelSchemas.getSchema(model, type)
    }
  },
  computed: {
    tables () {
      const schema = this.submission_type.submission_schema
      const order = schema.order.filter(f => (schema.properties[f].type) === 'table')
      return order.map(f => ({ id: f, label: schema.properties[f].title ? `${schema.properties[f].title} (${f})` : f }))
    }
  },
  watch: {
    modelValue: function (val) {
      alert('mapping changed')
      console.log('JSONMapper model value changed ', val)
      this.mapping = val
    }
  },
  components: { TableMapper }
}
</script>
