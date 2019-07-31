<template>
  <q-page class="q-pa-md q-gutter-md">
    <h4 class="text-center">Samples</h4>
    <SamplesTable/>
  </q-page>
</template>

<style>
</style>

<script>
import SamplesTable from '../components/tables/SamplesTable.vue'
export default {
  components: {
    SamplesTable
  }
}
</script>
