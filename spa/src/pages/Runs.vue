<template>
  <q-page class="">
    <BaseFormDialog ref="run_form" :form-component="RunForm" title="Create Run"/>
    <q-btn label="Create Run" @click="createRun"/>
    <!-- <RunForm/> -->
    <RunsTable/>
  </q-page>
</template>

<style>
</style>

<script>
import RunsTable from '../components/tables/RunsTable.vue'
import RunForm from '../components/forms/RunForm.vue'
import BaseFormDialog from '../components/dialogs/BaseFormDialog.vue'
export default {
  data () {
    return {
      RunForm: RunForm
    }
  },
  methods: {
    createRun () {
      this.$refs.run_form.open()
    },
    runCreated (request) {
      console.log('pool!', request.data)
      console.log('still here', this.$q, this.$refs)
      this.$q.notify('Run created.')
      this.$router.push({ name: 'run', params: { id: request.data.id } })
      this.$refs.run_form.$refs.dialog.close()
    }
  },
  components: {
    RunsTable,
    // RunForm,
    BaseFormDialog
  }
}
</script>
