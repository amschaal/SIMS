<template>
  <q-page class="">
    <h4 class="text-center">Pools</h4>
    <PoolFormDialog ref="pool_form" :model="{}" :onSuccess="poolCreated"/>
    <q-btn label="Create Pool" @click="openPoolDialog"/>
    <PoolsTable/>
  </q-page>
</template>

<style>
</style>

<script>
import PoolsTable from '../components/tables/PoolsTable.vue'
import PoolFormDialog from '../components/dialogs/PoolFormDialog.vue'
export default {
  methods: {
    openPoolDialog () {
      console.log(this.$refs.pool_form.$refs)
      this.$refs.pool_form.$refs.dialog.open()
    },
    poolCreated (request) {
      console.log('pool!', request.data)
      console.log('still here', this.$q, this.$refs)
      this.$q.notify('Pool created.')
      this.$router.push({ name: 'pool', params: { id: request.data.id } })
      this.$refs.pool_form.$refs.dialog.close()
    }
  },
  components: {
    PoolsTable,
    PoolFormDialog
  }
}
</script>
