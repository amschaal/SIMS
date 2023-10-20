<template>
  <q-page class="q-pa-sm q-gutter-sm">
    <h4 class="text-center">Libraries</h4>
    <LibrariesTable/>
  </q-page>
</template>

<style>
</style>

<script>
import LibrariesTable from '../components/tables/LibrariesTable.vue'
export default {
  components: {
    LibrariesTable
  }
}
</script>
