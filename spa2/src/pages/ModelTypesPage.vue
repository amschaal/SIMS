<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Model Types</h4>
    <q-select label="Select Model" :options="content_types"
        option-value="model"
        option-label="model"
        emit-value
        map-options
        v-model="model"
        outlined
      />
    <ModelTypesTable :filters="`&content_type__model=${model}`"/>
    <BaseFormDialog ref="create_form" :form-component="CreateModelTypeForm" title="Add Model Type"/>
    <q-btn label="Create" color="primary" @click="create"/>
  </q-page>
</template>

<style>
</style>

<script>
import ModelTypesTable from '../components/tables/ModelTypesTable.vue'
import BaseFormDialog from '../components/dialogs/BaseFormDialog.vue'
import CreateModelTypeForm from 'src/components/forms/CreateModelTypeForm.vue'
export default {
  data () {
    return {
      CreateModelTypeForm,
      content_types: [],
      model: this.$route.query.model
    }
  },
  methods: {
    create () {
      this.$refs.create_form.open()
    }
  },
  mounted () {
    this.$api.get('/api/content_types/?model__in=machine,project,sample,pool,run')
      .then(response => {
        this.content_types = response.data.results
      })
      .catch(error => {
        this.$q.notify({ message: 'Unable to fetch model content types' })
        console.log(error)
      })
  },
  components: {
    ModelTypesTable,
    BaseFormDialog
  }
}
</script>
