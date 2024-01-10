<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Pools</h4>
    <!-- <PoolFormDialog ref="pool_form_old" :model="{}" :onSuccess="poolCreated"/> -->
    <BaseFormDialog ref="pool_form" :form-component="PoolForm" title="Create Pool" :on-success="poolCreated"/>
    <q-btn label="Create Pool" color="primary" @click="openPoolDialog"/>
    <!-- <q-btn label="Create Pool" color="primary" @click="openPoolDialog"/> -->
    <PoolsTable/>
  </q-page>
</template>

<style>
</style>

<script>
import PoolsTable from '../components/tables/PoolsTable.vue'
// import PoolFormDialog from '../components/dialogs/PoolFormDialog.vue'
import PoolForm from '../components/forms/PoolForm.vue'
import BaseFormDialog from '../components/dialogs/BaseFormDialog.vue'
export default {
  props: [],
  data () {
    return {
      PoolForm
    }
  },
  methods: {
    openPoolDialog () {
      this.$refs.pool_form.open()
    },
    poolCreated (request) {
      this.$q.notify('Pool created.')
      this.$router.push({ name: 'pool', params: { id: request.data.id } })
      this.$refs.pool_form.$refs.dialog.close()
    }
  },
  components: {
    PoolsTable,
    // PoolFormDialog,
    BaseFormDialog
  }
}
</script>
