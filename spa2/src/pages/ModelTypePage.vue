<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h6 class="text-center"><router-link :to="{ name: 'model_types'}">Model Types</router-link> / {{id}}</h6>
    <div v-if="type">
    <BaseForm :api-url="`/api/model_types/${this.id}/`" api-method="put" v-model="type" :on-success="onSuccess" :on-error="onError">
      <template v-slot:content="{ model, errors, has_error }">
        <q-input outlined v-model="model.model" label="Model" :disable="true"/>
        <q-input outlined v-model="model.name" label="Name"
          :error-message="errors.name"
          :error="has_error.name"
          />
        <q-input outlined v-model="type.description" label="Description" />
        <JSONSchemaBuilder v-model="type.schema" :root-schema="type.schema" :options="{variables: options, showWidth: true}" type="submission"/>
        <!-- <q-btn label="Update" @click="submit" color="primary"/> -->
        schema: {{ type.schema }}
      </template>
    </BaseForm>
    </div>
  </q-page>
</template>

<style>
</style>

<script>
// import schemaForm from 'src/assets/jsonschema/forms/schemaForm.vue'
// import PoolFormDialog from '../components/forms/PoolFormDialog.vue'

import BaseForm from 'src/components/forms/BaseForm.vue'
export default {
  props: ['id'],
  data () {
    return {
      type: null,
      options: {}
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
    onSuccess () {
      this.$q.notify('The model was successfully updated')
    },
    onError () {
      this.$q.notify('There was an error updating the model')
    }
  },
  components: {
    BaseForm
  }
}
</script>
