<template>
  <q-page class="flex flex-center">
    <SubmissionTypeSelect v-model="submission_type"/><br>
    <!-- Submission Type: {{ submission_type }} -->
    <div v-if="submission_type">
    Variables: {{  schema_to_variables(submission_type.submission_schema) }}
    <q-markup-table flat bordered>
      <thead>
        <tr><th colspan="2">Source</th><th>Destination</th><th><TypeSelect v-model="type" :emit_object="true" :error_messages="{}" :has_error="false"/></th><th></th></tr>
        <tr>
          <th class="text-left">Variable</th>
          <th class="text-left">Name</th>
          <th></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="variable in schema_to_variables(submission_type.submission_schema)" :key="variable">
          <td class="text-left">{{variable}}</td>
          <td class="text-left">{{submission_type.submission_schema.properties[variable].title}}</td>
          <td> <q-select outlined v-model="mapping[variable]" :options="getOptions(type, mapping, submission_type.submission_schema.properties[variable].type)" label="Select Variable"
                option-value="id"
                option-label="label"
                emit-value
                />
          </td>
          <td></td>
        </tr>
      </tbody>
    </q-markup-table>
    {{ mapping }}
  </div>
  </q-page>
</template>

<style>
</style>

<script>
import SubmissionTypeSelect from 'src/components/SubmissionTypeSelect.vue'
import TypeSelect from 'src/components/TypeSelect.vue'

export default {
  data () {
    return {
      submission_type: null,
      type: null,
      mapping: {}
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
    }
  },
  // name: 'PageIndex',
  components: { SubmissionTypeSelect, TypeSelect }
}
</script>
