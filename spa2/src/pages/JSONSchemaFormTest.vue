<template>
  <q-page class="q-pa-sm q-gutter-sm">
    JSON Schema Form Test Page
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
                  />
    schema: {{ schema }}
  </q-page>
</template>

<style>
</style>

<script>
import JSONSchemaForm from 'src/assets/jsonschema/forms/JSONSchemaForm.vue'
export default {
  props: [],
  data () {
    return {
      schema_string: '',
      schema: null,
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
    }
  },
  components: {
    JSONSchemaForm
  }
}
</script>
