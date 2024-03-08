<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Machines</h4>
    <!-- <BaseFormDialog ref="machine_form" :form-component="MachineForm" title="Add Machine" :on-success="machineAdded" :on-error="machineError" :model="{}"/> -->
    <FormDialog ref="form_dialog" title="Create Machine" :on-success="machineAdded" :on-error="machineError" api-method="POST" api-url="/api/machines/">
      <template #form="props">
        <MachineForm v-model="props.data" :errors="props.errors"/>
      </template>
    </FormDialog>
    <q-btn label="Add Machine" color="primary" @click="addMachine"/>
    <!-- <RunForm/> -->
    <MachinesTable/>
  </q-page>
</template>

<style>
</style>

<script>
import MachinesTable from '../components/tables/MachinesTable.vue'
import MachineForm from '../components/forms/MachineForm.vue'
import FormDialog from '../components/dialogs/FormDialog.vue'
export default {
  data () {
    return {
    }
  },
  methods: {
    addMachine () {
      this.$refs.form_dialog.open()
    },
    machineAdded (request) {
      console.log('machine!', request.data)
      this.$q.notify('Machine added.')
      this.$router.push({ name: 'machine', params: { id: request.data.id } })
    },
    machineError (error) {
      if (error) {
        this.$q.notify({ color: 'negative', message: 'Error adding machine.' })
      }
    }
  },
  components: {
    MachinesTable,
    MachineForm,
    FormDialog
  }
}
</script>
