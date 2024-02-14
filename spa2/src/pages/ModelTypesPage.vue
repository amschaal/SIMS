<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Model Types</h4>
    <ModelTypesTable/>
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
      CreateModelTypeForm
    }
  },
  methods: {
    create () {
      this.$refs.create_form.open()
    }
  },
  components: {
    ModelTypesTable,
    BaseFormDialog
  }
}
</script>
