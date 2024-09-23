<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Runs</h4>
    <!-- <BaseFormDialog ref="run_form" :form-component="RunForm" title="Create Run" :on-success="runCreated" :on-error="runError"/> -->
    <FormDialog ref="form_dialog" title="Create Run" :on-success="runCreated" :on-error="runError" api-method="POST" api-url="/api/runs/">
      <template #form="props">
        <RunForm v-model="props.data" :errors="props.errors"/>
      </template>
    </FormDialog>
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
import FormDialog from '../components/dialogs/FormDialog.vue'
export default {
  data () {
    return {
    }
  },
  methods: {
    createRun () {
      this.$refs.form_dialog.open({})
    },
    runCreated (request) {
      // console.log('run!', request.data)
      // console.log('still here', this.$q, this.$refs)
      this.$q.notify('Run created.')
      this.$router.push({ name: 'run', params: { id: request.data.id } })
      // this.$refs.run_form.$refs.dialog.close()
    },
    runError (error) {
      if (error) {
        this.$q.notify({ color: 'negative', message: 'Error creating run.' })
      }
    }
  },
  components: {
    RunsTable,
    RunForm,
    FormDialog
  }
}
</script>
