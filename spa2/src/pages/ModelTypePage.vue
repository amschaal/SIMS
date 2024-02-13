<template>
  <q-page class="q-pa-sm q-gutter-sm">
    Model Type Page
    <div v-if="type">
    <q-input outlined v-model="type.name" label="Name"
        :error-message="error_messages.name"
        :error="has_error.name"
        />
    <q-input outlined v-model="type.description" label="Description" />
    <SchemaForm v-model="type.schema" :root-schema="type.schema" :options="{variables: options, showWidth: true}" type="submission"/>
    <q-btn label="Update" @click="submit" color="primary"/>
    schema: {{ type.schema }}
  </div>
  </q-page>
</template>

<style>
</style>

<script>
// import schemaForm from 'src/assets/jsonschema/forms/schemaForm.vue'
// import PoolFormDialog from '../components/forms/PoolFormDialog.vue'
import _ from 'lodash'
export default {
  props: ['id'],
  data () {
    return {
      type: null,
      options: {},
      errors: {}
    }
  },
  mounted: function () {
    this.$api
      .get(`/api/model_types/${this.id}/`)
      .then(response => {
        this.type = response.data
      })
  },
  methods: {
    submit () {
      this.$api.put(`/api/model_types/${this.id}/`, this.type)
        .then(response => {
          this.$q.notify('Model type updated')
          this.errors = {}
        })
        .catch(error => {
          if (error.response && error.response.data) {
            this.errors = error.response.data
            this.$q.notify('There was an error updating the model type')
          }
        })
    }
  },
  computed: {
    error_messages: function () {
      return _.mapValues(this.errors, function (e) { return Array.isArray(e) ? e.join(',') : '' })
    },
    has_error: function () {
      return _.mapValues(this.errors, function (e) { return e !== undefined })
    }
  },
  components: {
    // schemaForm
  }
}
</script>
