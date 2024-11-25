<template>
    <q-markup-table flat bordered dense>
      <span v-if="destSchema && destSchema.properties && destSchema.properties.data"></span>
      <thead>
        <tr><th colspan="3">Destination</th><th colspan="3">Source <q-btn label="I'm feeling lucky!" v-on:click="autoAssign()"></q-btn></th><th></th><th></th></tr>
        <tr>
          <th class="text-left">Destination Variable</th>
          <th class="text-left">Type</th>
          <th class="text-left">Name</th>
          <th class="text-left">Source Variable</th>
          <th class="text-left">Type</th>
          <th class="text-left">Name</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="variable in destVariables" :key="variable">
        <tr v-if="destSchema.properties[variable].type !== 'object'">
          <td class="text-left">{{variable}}</td>
          <td class="text-left">{{destSchema.properties[variable].type}}</td>
          <td class="text-left">{{destSchema.properties[variable].title}}</td>
          <td>
              <!-- getOptions(sourceSchema.properties.libraries.schema, mapping, destSchema.properties[variable].type) -->
              <q-select
                dense
                outlined
                v-model="mapping[variable]"
                :options="getFilteredOptions(destSchema.properties[variable].type)"
                label="Select Variable"
                option-value="id"
                option-label="label"
                emit-value
                @update:modelValue="val => selected(val)"
                :display-value="mapping[variable] ? `${variableObject[mapping[variable]].label}` : ''"
                >
                <template v-slot:after>
                  <q-btn @click="clearVariable(variable)" round icon="delete" v-if="mapping[variable]"/>
                </template>
              </q-select>
          </td>
          <!-- <td><span v-if="mapping.data && mapping.data[variable] && destSchema.properties[mapping.data[variable]]">{{destSchema.properties[mapping.data[variable]].type}}</span></td>
          <td><span v-if="mapping.data && mapping.data[variable] && destSchema.properties[mapping.data[variable]]">{{destSchema.properties[mapping.data[variable]].title}}</span></td> -->
        </tr>
        <tr v-else>
          <td>{{variable}}</td><td colspan="5">
            <TableMapper :source-schema="sourceSchema" v-model="mapping[variable]" v-if="mapping[variable]" :dest-schema="destSchema.properties[variable]" :table="table"/>
          </td>
        </tr>
        </template>
      </tbody>
    </q-markup-table>
</template>

<style>
</style>

<script>
// import SubmissionTypeSelect from 'src/components/SubmissionTypeSelect.vue'
// import TypeSelect from 'src/components/TypeSelect.vue'

export default {
  props: ['sourceSchema', 'modelValue', 'destSchema', 'table'],
  emits: ['update:modelValue'],
  data () {
    return {
      mapping: this.modelValue
    }
  },
  mounted () {
    this.schema_to_variables(this.destSchema).forEach(v => {
      if (this.destSchema.properties[v].type === 'object' && !this.mapping[v]) {
        this.mapping[v] = {}
      }
    })
    // if (!this.mapping.data) {
    //   this.mapping.data = {}
    // }
  },
  methods: {
    schema_to_variables (schema, path) {
      return path ? schema[path].order : schema.order
    },
    // getAvailableFields (schema, mapping, variableType) {
    //   const fieldTypes = variableType === 'table' ? ['table'] : ['number', 'string']
    //   return schema.order.filter(v => (!fieldTypes || fieldTypes.indexOf(schema.properties[v].type) !== -1))
    // },
    // getOptions (schema, mapping, variableType) {
    //   if (!schema) {
    //     return []
    //   }
    //   return this.getAvailableFields(schema, mapping, variableType).map(v => ({ id: `${this.table.id}[].${v}`, label: schema.properties[v].title || v }))
    // },
    getFilteredOptions (variableType) {
      const fieldTypes = variableType === 'array' ? ['array'] : ['number', 'string']
      return this.variableOptions.filter(o => (!fieldTypes || fieldTypes.indexOf(o.type) !== -1))
    },
    selected () {
      console.log('JSONTableMapper.selected', JSON.stringify(this.mapping))
      this.$emit('update:modelValue', this.mapping)
    },
    autoAssign () {
      alert(this.variableOptions.map(o => o.id))
      // const destVariables = this.schema_to_variables(this.destSchema)
      // this.schema_to_variables(this.sourceSchema).forEach(variable => {
      //   console.log(variable)
      //   if (!this.mapping[variable] && destVariables.indexOf(variable) !== -1) {
      //     console.log('assign', variable)
      //     this.mapping[variable] = variable
      //     this.selected(variable, variable)
      //   }
      // })
    },
    clearVariable (variable, path) {
      if (path) {
        delete this.mapping[path][variable]
      } else {
        delete this.mapping[variable]
      }
    }
  },
  computed: {
    variableOptions () {
      const options = []
      this.sourceSchema.order.forEach(v => {
        if (['array', 'table'].indexOf(this.sourceSchema.properties[v].type) === -1) {
          options.push({ id: v, variable: v, label: this.sourceSchema.properties[v].title || v, type: this.sourceSchema.properties[v].type })
        }
      })
      const tableSchema = this.sourceSchema.properties[this.table].items
      tableSchema.order.forEach(v => {
        const label = tableSchema.properties[v].title || v
        options.push({ id: `${this.table}.${v}`, variable: v, label: `${this.table} -> ${label}`, type: tableSchema.properties[v].type })
      })
      return options
    },
    variableObject () {
      const obj = {}
      this.variableOptions.forEach(o => {
        obj[o.id] = o
      })
      return obj
    },
    destVariables () {
      return this.schema_to_variables(this.destSchema)
    }
  },
  watch: {
    modelValue: function (val) {
      console.log('JSONTableMapper model value changed ', val)
      this.mapping = val
    }
  }
  // name: 'PageIndex',
  // components: { SubmissionTypeSelect, TypeSelect }
}
</script>
