<template>
  <q-page class="q-pa-sm q-gutter-sm">
    Model Type Page
    <SchemaForm v-model="type.schema" :root-schema="type.schema" :options="{variables: options, showWidth: true}" type="submission"/>
    schema: {{ type.schema }}
  </q-page>
</template>

<style>
</style>

<script>
// import schemaForm from 'src/assets/jsonschema/forms/schemaForm.vue'
// import PoolFormDialog from '../components/forms/PoolFormDialog.vue'
export default {
  props: [],
  data () {
    return {
      type: { schema: {} },
      options: {}
    }
  },
  methods: {
  },
  components: {
    // schemaForm
  }
}
</script>
