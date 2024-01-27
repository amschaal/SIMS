<template>
    <q-markup-table flat bordered>
      <thead>
        <tr><th colspan="3">Source</th><th colspan="3">Destination</th></tr>
        <tr>
          <th class="text-left">Source Variable</th>
          <th class="text-left">Type</th>
          <th class="text-left">Name</th>
          <th class="text-left">Destination Variable</th>
          <th class="text-left">Type</th>
          <th class="text-left">Name</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="variable in schema_to_variables(submission_type.submission_schema)" :key="variable">
        <tr>
          <td class="text-left">{{variable}}</td>
          <td class="text-left">{{submission_type.submission_schema.properties[variable].type}}</td>
          <td class="text-left">{{submission_type.submission_schema.properties[variable].title}}</td>
          <td> <q-select outlined v-model="mapping[variable]" :options="getOptions(type, mapping, submission_type.submission_schema.properties[variable].type)" label="Select Variable"
                option-value="id"
                option-label="label"
                emit-value
                @update:modelValue="val => selected(val, variable)"
                />
                <!-- <MappingTable :submission_type="submission_type" :type="type" v-model="mapping[variable]" v-if="submission_type.submission_schema.properties[variable].type === 'table'"/> -->
          </td>
          <td><span v-if="mapping[variable] && mapping[variable].variable">{{type.schema.properties[mapping[variable].variable].type}}</span></td>
          <td><span v-if="mapping[variable]  && mapping[variable].variable">{{type.schema.properties[mapping[variable].variable].title}}</span></td>
        </tr>
        <tr v-if="mapping[variable] && mapping[variable].mapping">
          <td></td><td colspan="5" ><JSONTableMapper :source-schema="submission_type.submission_schema.properties[variable].schema" :dest-schema="type.schema.properties[mapping[variable].variable].schema" v-model="mapping[variable].mapping"/></td>
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

// import SubmissionTypeSelect from 'src/components/SubmissionTypeSelect.vue'
// import TypeSelect from 'src/components/TypeSelect.vue'

export default {
  props: ['submission_type', 'type', 'modelValue'],
  emits: ['update:modelValue'],
  data () {
    return {
      mapping: this.modelValue
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
        this.mapping[variable] = { variable: val, mapping: {} }
      }
      // console.log(val, variable, this.type.schema.properties, this.mapping[variable].variable)
      this.$emit('update:modelValue', this.mapping)
    }
  },
  components: { JSONTableMapper }
}
</script>
