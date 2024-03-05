<template>
  <q-page class="q-pa-sm q-gutter-sm">
    JSON Schema Form Test Page
    <JSONSchemaBuilder v-model="builder_schema" :root-schema="builder_schema" :options="{showWidth: true}" type="submission"/>
    <q-btn @click="updateSchemaFromBuilder" label="Update"/>
    <q-input
      outlined
      v-model="schema_string"
      label="Schema"
      filled
      type="textarea"
        />
    <q-btn @click="updateSchema" label="Update"/>
    <JSONSchemaForm
                  v-if="schema"
                  v-model="data"
                  :schema="schema"
                  :editable="true"
                  :modify="true"
                  :warnings="warnings"
                  :errors="errors"
                  >
            <template #field_test="{ v, data, form }">
              <div>
                <q-input type="textarea" v-model="data[v.variable]" label="OVERRIDDEN!!"/>
                {{ form.colWidth(v) }} <!-- proof of concept that you can access form's functions, data, etc -->
              </div>
            </template>
    </JSONSchemaForm>
    <div>schema: {{ schema }}</div>
    <div>Data: {{ data }}</div>
  </q-page>
</template>

<style>
</style>

<script>
import JSONSchemaForm from 'src/assets/jsonschema/components/forms/JSONSchemaForm.vue'
import _ from 'lodash'
export default {
  props: [],
  data () {
    return {
      schema_string: '',
      builder_schema: {},
      schema: {},
      data: {},
      errors: {},
      warnings: {}
    }
  },
  mounted: function () {
  },
  methods: {
    updateSchema () {
      this.schema = JSON.parse(this.schema_string)
    },
    updateSchemaFromBuilder () {
      this.schema = _.cloneDeep(this.builder_schema)
      this.schema_string = JSON.stringify(this.builder_schema)
    }
  },
  components: {
    JSONSchemaForm
  }
}
</script>
