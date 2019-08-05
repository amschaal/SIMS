<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Machines</h4>
    <BaseFormDialog ref="machine_form" :form-component="MachineForm" title="Add Machine" :on-success="machineAdded" :on-error="machineError"/>
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
import BaseFormDialog from '../components/dialogs/BaseFormDialog.vue'
export default {
  data () {
    return {
      MachineForm: MachineForm
    }
  },
  methods: {
    addMachine () {
      this.$refs.machine_form.open()
    },
    machineAdded (request) {
      console.log('machine!', request.data)
      this.$q.notify('Machine added.')
      this.$router.push({ name: 'machine', params: { id: request.data.id } })
      this.$refs.machine_form.$refs.dialog.close()
    },
    machineError (error) {
      if (error) {
        this.$q.notify({ color: 'negative', message: 'Error adding machine.' })
      }
    }
  },
  components: {
    MachinesTable,
    // RunForm,
    BaseFormDialog
  }
}
</script>
