<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Model Types</h4>
    <ModelTypesTable/>
  </q-page>
</template>

<style>
</style>

<script>
import ModelTypesTable from '../components/tables/ModelTypesTable.vue'
// import BaseFormDialog from '../components/dialogs/BaseFormDialog.vue'
export default {
  data () {
    return {
      // ModelTypeForm
    }
  },
  methods: {
  },
  components: {
    ModelTypesTable
  }
}
</script>
