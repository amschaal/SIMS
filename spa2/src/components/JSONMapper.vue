<template>
    <q-markup-table flat bordered dense>
      <thead>
        <tr><th colspan="3">Source</th><th colspan="3">Destination <q-btn label="I'm feeling lucky!" v-on:click="autoAssign()"></q-btn></th></tr>
        <tr>
          <th class="text-left" style="width: 10%;">Source Variable</th>
          <th class="text-left">Type</th>
          <th class="text-left">Name</th>
          <th class="text-left">Destination Variable</th>
          <th class="text-left">Type</th>
          <th class="text-left">Name</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="variable in schema_to_variables(submission_type.submission_schema)" :key="variable">
        <tr v-if="submission_type.submission_schema.properties[variable].type === 'table'">
          <td class="text-left" style="width: 10%;">{{variable}}</td>
          <td class="text-left">{{submission_type.submission_schema.properties[variable].type}}</td>
          <td class="text-left">{{submission_type.submission_schema.properties[variable].title}}</td>
          <td colspan="3">
            <q-select dense outlined v-model="mapping[variable]" :options="mapping_types" label="Select Mapping Type"
                option-value="id"
                option-label="label"
                @update:modelValue="val => selectMappingType(val, variable)"
                >
                <template v-slot:after v-if="mapping[variable]">
                  <q-btn @click="clearTableVariable(variable)" round icon="delete"></q-btn>
                </template>
            </q-select>
                <!-- :modelValue="pageTitle"
  @update:modelValue="pageTitle = $event" -->
            <!-- <TypeSelect :error_messages="{}" :has_error="{}" v-model="mapping[variable].model_type" @update:model-value="val => selectedModelType(val, variable)" :emit_object="true" v-if="mapping[variable] && mapping[variable].mapping_type === 'model'"/> -->
              <TypeSelect :dense="true" :error_messages="{}" :has_error="{}" :modelValue="mapping[variable].model_type" @update:model-value="val => selectedModelType(val, variable)" :emit_object="true" v-if="mapping[variable] && mapping[variable].mapping_type === 'model'" :model-filter="mapping[variable].model"/>
          </td>
        </tr>
        <tr v-else>
          <td class="text-left" style="width: 10%;">{{variable}}</td>
          <td class="text-left">{{submission_type.submission_schema.properties[variable].type}}</td>
          <td class="text-left">{{submission_type.submission_schema.properties[variable].title}}</td>
          <td> <q-select dense outlined v-model="mapping[variable]" :options="getOptions(type, mapping, submission_type.submission_schema.properties[variable].type)" label="Select Variable"
                option-value="id"
                option-label="label"
                emit-value
                @update:modelValue="val => selected(val, variable)"
                >
                <template v-slot:after v-if="mapping[variable]">
                  <q-btn @click="clearVariable(variable)" round icon="delete"></q-btn>
                </template>
                </q-select>
                <!-- <MappingTable :submission_type="submission_type" :type="type" v-model="mapping[variable]" v-if="submission_type.submission_schema.properties[variable].type === 'table'"/> -->
          </td>
          <td><span v-if="mapping[variable] && mapping[variable].variable">{{type.schema.properties[mapping[variable].variable].type}}</span></td>
          <td><span v-if="mapping[variable]  && mapping[variable].variable">{{type.schema.properties[mapping[variable].variable].title}}</span></td>
        </tr>
        <tr v-if="mapping[variable] && mapping[variable].mapping && variable_schemas[variable]">
          <td>
            Fix: This should actually be mapping to another schema which must be selected.<br>
            For example, a schema for "RNA libraries", etc.
          </td>
          <td colspan="5" >
            <!-- <JSONTableMapper :source-schema="submission_type.submission_schema.properties[variable].schema" :dest-schema="type.schema.properties[mapping[variable].variable].schema" v-model="mapping[variable].mapping"/> -->
            <JSONTableMapper :source-schema="submission_type.submission_schema.properties[variable].schema" :dest-schema="variable_schemas[variable]" v-model="mapping[variable].mapping" />
          </td>
        </tr>
      </template>
      </tbody>
      <!-- {{ type }} -->
    </q-markup-table>
</template>

<style>
</style>

<script>
import JSONTableMapper from './JSONTableMapper.vue'
import TypeSelect from 'src/components/TypeSelect.vue'
// import SubmissionTypeSelect from 'src/components/SubmissionTypeSelect.vue'
// import TypeSelect from 'src/components/TypeSelect.vue'

export default {
  props: ['submission_type', 'type', 'modelValue'],
  emits: ['update:modelValue'],
  data () {
    return {
      mapping: this.modelValue,
      variable_schemas: {},
      mapping_types: [{ id: 'JSON', label: 'JSON' }, { id: 'samples', model: 'sample', label: 'Samples', schema_url: '/api/samples/jsonschema/' }, { id: 'pools', model: 'pool', label: 'Pools', schema_url: '/api/pools/jsonschema/' }]
    }
  },
  methods: {
    schema_to_variables (schema, path) {
      return schema.order
    },
    getAvailableFields (type, mapping, variableType) {
      const usedVariables = Object.values(mapping)
      const fieldTypes = variableType === 'table' ? ['table'] : ['number', 'string']
      return type.schema.order.filter(v => usedVariables.indexOf(v) < 0 && (!fieldTypes || fieldTypes.indexOf(type.schema.properties[v].type) !== -1))
    },
    getOptions (type, mapping, variableType) {
      if (!type || !type.schema) {
        return []
      }
      return this.getAvailableFields(type, mapping, variableType).map(v => ({ id: v, label: type.schema.properties[v].title || v }))
    },
    selected (val, variable) {
      if (this.submission_type.submission_schema.properties[variable].type === 'table') {
        console.log('selected: overwriting mapping')
        this.mapping[variable] = { variable: val, mapping: {} }
      }
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
    selectedModelType (type, variable) {
      console.log('selectedModelType', type, variable, this.mapping[variable])
      console.log(`/api/${this.mapping[variable].model}/jsonschema/`)
      this.$api.post(`/api/${this.mapping[variable].model}/jsonschema/`, { type: type.id })
      // Object.getOwnPropertyNames(this.mapping[variable].mapping).forEach(prop => delete this.mapping[variable].mapping[prop])
      // this.mapping[variable].mapping = {}
      if (this.mapping[variable] && this.mapping[variable].model_type !== type.id) {
        console.log('selectModelType clear mapping')
        Object.getOwnPropertyNames(this.mapping[variable].mapping).forEach(prop => delete this.mapping[variable].mapping[prop])
      }
      this.mapping[variable].model_type = type.id
      this.variable_schemas[variable] = type.schema
      // alert(JSON.stringify(this.mapping[variable]))
      this.$emit('update:modelValue', this.mapping)
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
    }
  },
  watch: {
    modelValue: function (val) {
      alert('mapping changed')
      console.log('JSONMapper model value changed ', val)
      this.mapping = val
    }
  },
  components: { JSONTableMapper, TypeSelect }
}
</script>
