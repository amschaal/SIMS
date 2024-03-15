<template>
  <!-- <q-page class="flex flex-center"> -->
  <q-page>
    From: <SubmissionTypeSelect v-model="submission_type" @update:model-value="setMapping(type)"/>
    To: <TypeSelect v-model="type" :emit_object="true" :error_messages="{}" :has_error="false" model-filter="project"/><br>
    <!-- Submission Type: {{ submission_type }} -->
    <div v-if="submission_type">
    Variables: {{  schema_to_variables(submission_type.submission_schema) }}
    <!-- <q-markup-table flat bordered>
      <thead>
        <tr><th colspan="2">Source</th><th>Destination</th><th></th><th></th></tr>
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
    </q-markup-table> -->
    <JSONMapper v-model="mapping" :submission_type="submission_type" :type="type" v-if="submission_type && type"/>
    <q-btn label="Update Mapping" @click="updateMapping" v-if="submission_type.id"/>
    {{ mapping }}
  </div>
  </q-page>
</template>

<style>
</style>

<script>
import JSONMapper from 'src/components/JSONMapper.vue'
import SubmissionTypeSelect from 'src/components/SubmissionTypeSelect.vue'
import TypeSelect from 'src/components/TypeSelect.vue'
import _ from 'lodash'

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
    },
    updateMapping () {
      this.$api
        .post(`/api/submission_types/${this.submission_type.id}/update_mapping/`, { mapping: this.mapping })
        .then(response => {
          this.options = response.data.results
          this.submission_type.mapping = this.mapping
        })
    },
    setMapping (type) {
      console.log('setMapping', this.submission_type.mapping, JSON.stringify(this.submission_type.mapping))
      this.mapping = _.cloneDeep(this.submission_type.mapping)
    }
  },
  watch: {
    mapping: {
      handler (val, oldVal) {
        console.log('MapTypesPage.mapping model value changed ', JSON.stringify(val))
        console.log('old value', JSON.stringify(oldVal))
      },
      deep: true
    }
  },
  // name: 'PageIndex',
  components: { SubmissionTypeSelect, TypeSelect, JSONMapper }
}
</script>
