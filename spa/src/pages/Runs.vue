<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Runs</h4>
    <BaseFormDialog ref="run_form" :form-component="RunForm" title="Create Run" :on-success="runCreated" :on-error="runError"/>
    <q-btn label="Create Run" color="primary" @click="createRun"/>
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
      console.log('run!', request.data)
      console.log('still here', this.$q, this.$refs)
      this.$q.notify('Run created.')
      this.$router.push({ name: 'run', params: { id: request.data.id } })
      this.$refs.run_form.$refs.dialog.close()
    },
    runError (error) {
      if (error) {
        this.$q.notify({ color: 'negative', message: 'Error creating run.' })
      }
    }
  },
  components: {
    RunsTable,
    // RunForm,
    BaseFormDialog
  }
}
</script>
