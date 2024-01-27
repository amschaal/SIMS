<template>
    <q-markup-table flat bordered>
      <thead>
        <tr><th colspan="3">Source</th><th colspan="3">Destination</th><th></th><th></th></tr>
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
        <tr v-for="variable in schema_to_variables(sourceSchema)" :key="variable">
          <td class="text-left">{{variable}}</td>
          <td class="text-left">{{sourceSchema.properties[variable].type}}</td>
          <td class="text-left">{{sourceSchema.properties[variable].title}}</td>
          <td> <q-select outlined v-model="mapping[variable]" :options="getOptions(destSchema, mapping, sourceSchema.properties[variable].type)" label="Select Variable"
                option-value="id"
                option-label="label"
                emit-value
                @update:modelValue="val => selected(val)"
                />
                <!-- <MappingTable :submission_type="submission_type" :type="type" v-model="mapping[variable]" v-if="submission_type.submission_schema.properties[variable].type === 'table'"/> -->
          </td>
          <td><span v-if="mapping[variable]">{{destSchema.properties[mapping[variable]].type}}</span></td>
          <td><span v-if="mapping[variable]">{{destSchema.properties[mapping[variable]].title}}</span></td>
        </tr>
      </tbody>
    </q-markup-table>
</template>

<style>
</style>

<script>
// import SubmissionTypeSelect from 'src/components/SubmissionTypeSelect.vue'
// import TypeSelect from 'src/components/TypeSelect.vue'

export default {
  props: ['sourceSchema', 'modelValue', 'destSchema'],
  emits: ['update:modelValue'],
  data () {
    return {
      mapping: this.modelValue
    }
  },
  // mounted () {

  // },
  methods: {
    schema_to_variables (schema, path) {
      return schema.order
    },
    getAvailableFields (schema, mapping, variableType) {
      const usedVariables = Object.values(mapping)
      const fieldTypes = variableType === 'table' ? ['table'] : ['number', 'string']
      return schema.order.filter(v => usedVariables.indexOf(v) < 0 && (!fieldTypes || fieldTypes.indexOf(schema.properties[v].type) !== -1))
    },
    getOptions (schema, mapping, variableType) {
      if (!schema) {
        return []
      }
      return this.getAvailableFields(schema, mapping, variableType).map(v => ({ id: v, label: schema.properties[v].title || v }))
    },
    selected () {
      this.$emit('update:modelValue', this.mapping)
    }
  }
  // name: 'PageIndex',
  // components: { SubmissionTypeSelect, TypeSelect }
}
</script>
