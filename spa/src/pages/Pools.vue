<template>
  <q-page class="">
    <h4 class="text-center">Pools</h4>
    <PoolFormDialog ref="pool_form" :model="{}"/>
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
    }
  },
  components: {
    PoolsTable,
    PoolFormDialog
  }
}
</script>
