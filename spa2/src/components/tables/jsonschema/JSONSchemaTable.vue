<!-- eslint-disable vue/no-mutating-props -->
<template>
  <q-field
    v-if="schema && schema.order && schema.order.length"
    :hint="''"
    class="q-pb-xl q-mb-xl"
    borderless
    bottom-slots
    :error="hasError()"
  >
    <!-- <Samplesheet v-model="submission.sample_data" :type="type"/> -->
    <template v-slot:control>
      <!-- :submission="submission"
      v-on:warnings="updateWarnings"
      v-on:errors="updateErrors" -->
      <!-- :editable="modify && ($store.getters.isStaff || !v.schema.internal)" -->
      <AgSchema
        v-model="data"
        :schema="schema"
        :editable="modify"
        :allow-examples="true"
        :allow-force-save="true"
        ref="agschema"
        :table-warnings="getWarnings()"
        :table-errors="getErrors()"
        :admin="true"
        />
      <q-btn :label="table_button_label()"  @click="openTable()" />
    </template>
    <template v-slot:error>
      <div v-if="hasError()">{{getError()}}</div>
      <div v-if="hasWarning()" class="warning">Table contains warnings</div>
    </template>
  </q-field>

</template>

<script>
// import { QSelect, QOptionGroup, QCheckbox, QInput } from 'quasar'
import AgSchema from 'src/assets/jsonschema/components/aggrid/agschema.vue'
// import _ from 'lodash'

export default {
  props: ['modelValue', 'schema', 'editable', 'errors', 'warnings', 'modify', 'ui', 'title'],
  data () {
    return {
      data: this.modelValue ? this.modelValue : {}
    }
  },
  setup (props) {
    console.log('setting up', props.schema, props)
  },
  mounted () {
    console.log('JSONSchemaTable Mounted', this.schema, this.modelValue)
  },
  methods: {
    getError () {
      // console.log('getError1', v.schema, v.schema.error_message, this.errors, v.variable)
      let errors = this.schema.error_message ? this.schema.error_message : this.errors
      if (Array.isArray(errors)) {
        errors = errors.map(e => (typeof e === 'string' ? e : 'Table contains errors.'))
      }
      return errors && errors.join ? errors.join(', ') : errors
    },
    hasError () {
      return this.errors
    },
    getWarning (flatten) {
      const warning = this.schema.error_message || this.warnings
      return warning && warning.join ? warning.join(', ') : ''
    },
    hasWarning () {
      return this.warnings !== undefined
    },
    getWarnings () {
      return this.warnings ? this.warnings : {}
    },
    getErrors () {
      return this.errors ? this.errors : {}
    },
    setValue (type, value, variable, val, e) {
      if (value.cancelBubble) {
        alert('cancel bubble')
        value.cancelBubble = true
      } else if (!value.target) {
        // console.log('set', this.value[variable], val)
        // this.value[variable] = val
        this.data = val
      }
      console.log('setValue', type, value, variable, val, e, this.value)
    },
    openTable () {
      // console.log('refs', this.$refs, v, this.$refs[v.variable][0])
      this.$refs.agschema.openSamplesheet()
    },
    table_button_label () {
      // console.log('table_button_label', v, v.variable, this.value, this.value[v.variable])
      return this.schema.title
    }
    // ,
    // tableHint (v) {
    //   if (v.schema.items.description) {
    //     return v.schema.items.description
    //   } else {
    //     return (v.schema.title ? v.schema.title : v.variable) + ': Click on the button above to open the table'
    //   }
    // }
  },
  computed: {
    value () {
      return this.modelValue
    }
  },
  components: {
    AgSchema // AgSchema: () => import('../agschema.vue')
    // AgSchema: () => import('../agschema.vue')
  },
  watch: {
  }
}
</script>
<style scoped>
.q-field {
  padding: 3px !important;
}
.warning {
  color: orange;
}
p.caption {
  font-weight: bold;
}
</style>
